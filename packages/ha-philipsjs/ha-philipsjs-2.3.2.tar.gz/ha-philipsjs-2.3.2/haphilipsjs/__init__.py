from typing import Any, Dict, Literal, Optional, Tuple, TypeVar, Union, cast
import httpx
import logging
import warnings
import json
from urllib.parse import quote
from secrets import token_bytes, token_hex
from base64 import b64decode, b64encode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hmac import HMAC

from .typing import ActivitesTVType, ApplicationIntentType, ApplicationsType, ChannelDbTv, ChannelListType, ChannelsCurrentType, ChannelsType, ContextType, FavoriteListType, SystemType, ApplicationType

LOG = logging.getLogger(__name__)
TIMEOUT = 5.0
TIMEOUT_POOL = 20
TIMEOUT_NOTIFYREAD = 130
DEFAULT_API_VERSION = 1

AUTH_SHARED_KEY = b64decode("ZmVay1EQVFOaZhwQ4Kv81ypLAZNczV9sG4KkseXWn1NEk6cXmPKO/MCa9sryslvLCFMnNe4Z4CPXzToowvhHvA==")
"""Key used for hmac signatures and decoding of cbc data."""

TV_PLAYBACK_INTENTS = [
    {
        'component': {
            'className': 'org.droidtv.playtv.PlayTvActivity',
            'packageName': 'org.droidtv.playtv'
        }
    }
]

def hmac_signature(key: bytes, timestamp: str, data: str):
    """Calculate a timestamped signature."""
    hmac = HMAC(key, SHA256())
    hmac.update(timestamp.encode("utf-8"))
    hmac.update(data.encode("utf-8"))
    return b64encode(hmac.finalize()).decode("utf-8")

def cbc_decode(key: bytes, data: str):
    """Decoded encrypted fields based on shared key."""
    if data == "":
        return ""
    raw = b64decode(data)
    assert len(raw) >= 16, f"Lenght of data too short: '{data}'"
    decryptor = Cipher(algorithms.AES(key[0:16]), modes.CBC(raw[0:16])).decryptor()
    unpadder = PKCS7(128).unpadder()
    result = decryptor.update(raw[16:]) + decryptor.finalize()
    result = unpadder.update(result) + unpadder.finalize()
    return result.decode("utf-8")

def cbc_encode(key: bytes, data: str):
    """Decoded encrypted fields based on shared key."""
    raw = data.encode("utf-8")
    iv = token_bytes(16)
    encryptor = Cipher(algorithms.AES(key[0:16]), modes.CBC(iv)).encryptor()
    padder = PKCS7(128).padder()
    result = padder.update(raw) + padder.finalize()
    result = encryptor.update(result) + encryptor.finalize()
    return b64encode(iv + result).decode("utf-8")

def decode_xtv_json(text: str):
    if text == "" or text == "}":
        LOG.debug("Ignoring invalid json %s", text)
        return {}

    try:
        data = json.loads(text)
    except json.decoder.JSONDecodeError:
        LOG.debug("Invalid json received, trying adjusted version")
        text = text.replace("{,", "{")
        text = text.replace(",}", "}")
        while (p:= text.find(",,")) >= 0:
            text = text[:p] + text[p+1:]
        data = json.loads(text)

    return data

PASSTHROUGH_URI = "content://android.media.tv/passthrough"
def passthrough_uri(data):
    return f"{PASSTHROUGH_URI}/{quote(data, safe='')}"

CHANNEL_URI = "content://android.media.tv/channel"
def channel_uri(channel):
    uri = CHANNEL_URI
    if channel is not None:
        uri += f"/{channel}"
    return uri

class GeneralFailure(Exception):
    """Base class for component failures."""

class ConnectionFailure(GeneralFailure):
    """Failed to connect to tv it's likely turned off."""

class ProtocolFailure(GeneralFailure):
    """Wrapper to contain erros that are the server closing a connection before response."""

class PairingFailure(GeneralFailure):
    def __init__(self, data):
        super().__init__(f"Failed to start pairing: {data}")
        self.data = data

class NoneJsonData(GeneralFailure):
    def __init__(self, data):
        super().__init__(f"Non json data received: {data}")
        self.data = data
    """API Returned non json data when json was expected."""


T = TypeVar('T') 

class PhilipsTV(object):

    def __init__(self, host=None, api_version=DEFAULT_API_VERSION, secured_transport=None, username=None, password=None, verify=False, auth_shared_key=None):
        self._host = host
        self._connfail = 0
        self.api_version = int(api_version)
        self.on = False
        self.name: Optional[str] = None
        self.system: Optional[SystemType] = None
        self.sources = {}
        self.source_id = None
        self.audio_volume = None
        self.channels: ChannelsType = {}
        self.channel: Optional[Union[ActivitesTVType, ChannelsCurrentType]] = None
        self.channel_lists: Dict[str, ChannelListType] = {}
        self.favorite_lists: Dict[str, FavoriteListType] = {}
        self.applications: Dict[str, ApplicationType] = {}
        self.application: Optional[ApplicationIntentType] = None
        self.context: Optional[ContextType] = None
        self.screenstate: Optional[str] = None
        self.ambilight_topology = None
        self.ambilight_mode = None
        self.ambilight_cached = None
        self.ambilight_measured = None
        self.ambilight_processed = None
        self.powerstate = None
        if auth_shared_key:
            self.auth_shared_key = auth_shared_key
        else:
            self.auth_shared_key = AUTH_SHARED_KEY

        if secured_transport:
            self.protocol = "https"
            self.port = 1926
        else:
            self.protocol = "http"
            self.port = 1925

        timeout = httpx.Timeout(timeout=TIMEOUT, pool=TIMEOUT_POOL)
        limits = httpx.Limits(max_keepalive_connections=1, max_connections=2)
        self.session = httpx.AsyncClient(limits=limits, timeout=timeout, verify=False)
        self.session.headers["Accept"] = "application/json"

        if username and password:
            self.session.auth = httpx.DigestAuth(username, password)

    @property
    def quirk_playpause_spacebar(self):
        """Does this tv need workaround for playpause."""
        if self.system:
            return self.system.get("os_type", "").startswith("MSAF_")
        else:
            return None

    @property
    def pairing_type(self):
        if self.system:
            return self.system.get("featuring", {}).get("systemfeatures", {}).get("pairing_type")
        else:
            return None

    @property
    def secured_transport(self) -> Optional[bool]:
        if self.system:
            return self.system.get("featuring", {}).get("systemfeatures", {}).get("secured_transport") == "true"
        else:
            return None

    @property
    def notify_change_supported(self) -> Optional[str]:
        if self.system:
            return self.system.get("notifyChange", None)
        else:
            return None

    def json_feature_supported(self, type: str, value: Optional[str]):
        if self.system:
            features = self.system.get("featuring", {}).get("jsonfeatures", {}).get(type, [])
            if value:
                return value in features
            else:
                return features
        else:
            return None

    @property
    def api_version_detected(self) -> Optional[int]:
        if self.system:
            return self.system.get("api_version", {}).get("Major")
        else:
            return None

    @property
    def channel_active(self):
        if self.context and "level1" in self.context:
            return self.context["level1"] in ("WatchTv", "WatchSatellite")
        if self.context and "activity" in self.context:
            return self.context["activity"] in ("WatchTv", "WatchSatellite")
        if self.application:
            return self.application in TV_PLAYBACK_INTENTS
        if self.source_id in ("tv", "11", None):
            return self.channel_id is not None
        return False

    @property
    def application_id(self):
        if self.application and "component" in self.application:
            component = self.application["component"]
            app_id = f"{component.get('className', 'None')}-{component.get('packageName', 'None')}"
            if app_id in self.applications:
                return app_id
            else:
                return None
        else:
            return None

    @property
    def min_volume(self):
        if self.audio_volume:
            return int(self.audio_volume['min'])
        else:
            return None

    @property
    def max_volume(self):
        if self.audio_volume:
            return int(self.audio_volume['max'])
        else:
            return None

    @property
    def volume(self):
        if self.audio_volume and int(self.audio_volume['max']):
            return self.audio_volume['current'] / int(self.audio_volume['max'])
        else:
            return None

    @property
    def muted(self):
        if self.audio_volume:
            return self.audio_volume['muted']
        else:
            return None

    @property
    def channel_id(self):
        if self.api_version >= 5:
            r = cast(Optional[ActivitesTVType], self.channel)
            if r and r['channel']:
                # it could be empty if HDMI is set
                return str(r['channel']['ccid'])
            else:
                return None
        else:
            r = cast(Optional[ChannelsCurrentType], self.channel)
            if not r:
                return None

            if not self.channels.get(r['id']):
                pos = r['id'].find('_')
                if pos > 0:
                    return r['id'][pos+1:]
            return r['id']

    async def aclose(self) -> None:
        await self.session.aclose()

    def _url(self, path):
        return f'{self.protocol}://{self._host}:{self.port}/{self.api_version}/{path}'

    async def _getReq(self, path) -> Optional[Dict]:

        try:
            resp = await self.session.get(self._url(path), timeout=TIMEOUT)
            if resp.status_code != 200:
                return None
            return decode_xtv_json(resp.text)
        except (httpx.ConnectTimeout, httpx.ConnectError) as err:
            raise ConnectionFailure(err) from err
        except httpx.HTTPError as err:
            raise GeneralFailure(err) from err        

    async def _getBinary(self, path: str) -> Tuple[Optional[bytes], Optional[str]]:

        try:
            resp = await self.session.get(self._url(path), timeout=TIMEOUT)
            if resp.status_code != 200:
                return None, None
            return resp.content, resp.headers.get("content-type")
        except (httpx.ConnectTimeout, httpx.ConnectError) as err:
            raise ConnectionFailure(err) from err
        except httpx.HTTPError as err:
            raise GeneralFailure(err) from err

    async def _postReq(self, path: str, data: Dict, timeout=TIMEOUT) -> Optional[Dict]:
        try:
            resp = await self.session.post(self._url(path), json=data, timeout=timeout)
            if resp.status_code == 200:
                LOG.debug("Post succeded: %s -> %s", data, resp.text)
                if resp.headers.get('content-type', "").startswith("application/json"):
                    return decode_xtv_json(resp.text)
                else:
                    return {}
            else:
                LOG.warning("Post failed: %s -> %s", data, resp.text)
                return None
        except httpx.ReadTimeout:
            LOG.debug("Read time out on postReq", exc_info=True)
            return None
        except (httpx.ConnectTimeout, httpx.ConnectError) as err:
            raise ConnectionFailure(err) from err
        except httpx.ProtocolError as err:
            raise ProtocolFailure(err) from err
        except httpx.HTTPError as err:
            raise GeneralFailure(err) from err

    async def pairRequest(self, app_id: str, app_name: str, device_name: str, device_os: str, type: str, device_id: Optional[str] = None):
        """Start up a pairing request."""
        if device_id is None:
            device_id = token_hex(16)

        device = {
            "device_name": device_name,
            "device_os": device_os,
            "type" : type,
            "id": device_id,
            "app_id": app_id,
            "app_name": app_name,
        }

        state = {
            "device": device
        }

        data = {
            "scope" : [
                "read",
                "write",
                "control"
            ],
            "device": device
        }

        LOG.debug("pair/request request: %s", data)
        resp = await self.session.post(self._url("pair/request"), json=data, auth=None)
        if not resp.headers['content-type'].startswith("application/json"):
            raise NoneJsonData(resp.text)
        data_response = resp.json()

        LOG.debug("pair/request response: %s", data_response)
        if data_response.get("error_id") != "SUCCESS":
            raise PairingFailure(data_response)

        state["timestamp"] = data_response["timestamp"]
        state["auth_key"] = data_response["auth_key"]

        return state

    async def pairGrant(self, state: Dict[str, Any], pin: str):
        """Finish a pairing sequence"""
        auth_handler = httpx.DigestAuth(
            state["device"]["id"],
            state["auth_key"]
        )

        signature = hmac_signature(
            self.auth_shared_key,
            str(state['timestamp']),
            pin
        )

        auth = {
            "auth_appId" : "1",
            "auth_timestamp": state["timestamp"],
            "auth_signature": signature,
            "pin": pin,
        }

        data = {
            "auth": auth,
            "device": state["device"]
        }

        LOG.debug("pair/grant request: %s", data)
        resp = await self.session.post(self._url("pair/grant"), json=data, auth=auth_handler)
        if not resp.headers['content-type'].startswith("application/json"):
            raise NoneJsonData(resp.text)
        data_response = resp.json()
        LOG.debug("pair/grant response: %s", data_response)

        if data_response.get("error_id") != "SUCCESS":
            raise PairingFailure(data_response)

        self.session.auth = auth_handler
        return state["device"]["id"], state["auth_key"]

    async def setTransport(self, secured_transport: Optional[bool] = None, api_version: Optional[int] = None):
        if secured_transport == True and self.protocol != "https":
            LOG.info("Switching to secured transport")
            self.protocol = "https"
            self.port = 1926
        elif secured_transport == False and self.protocol != "http":
            LOG.info("Switching to unsecured transport")
            self.protocol = "http"
            self.port = 1925

        if api_version and api_version != self.api_version:
            LOG.info("Switching to api_version %d", api_version)
            self.api_version = api_version


    async def update(self):
        try:
            if not self.on:
                await self.getSystem()
                await self.setTransport(self.secured_transport)
                await self.getSources()
                await self.getChannelLists()
                await self.getChannels()
                await self.getApplications()

            await self.getPowerState()
            await self.getAudiodata()
            await self.getSourceId()
            await self.getChannelId()
            await self.getApplication()
            await self.getContext()
            await self.getScreenState()
            self.on = True
            return True
        except ConnectionFailure as err:
            LOG.debug("TV not available: %s", repr(err))
            self.on = False
            return False

    def _decodeSystem(self, system) -> SystemType:
        result = {}
        for key, value in system.items():
            if key.endswith("_encrypted"):
                result[key[:-10]] = cbc_decode(self.auth_shared_key, value)
            else:
                result[key] = value
        return cast(SystemType, result)

    async def getSystem(self):
        r = cast(Optional[SystemType], await self._getReq('system'))
        if r:
            self.system = self._decodeSystem(r)
            self.name = r['name']
        else:
            self.system = {}
            self.name = None
        return r

    async def getAudiodata(self):
        r = await self._getReq('audio/volume')
        if r:
            self.audio_volume = r
        else:
            self.audio_volume = r
        return r

    async def getChannels(self):
        if self.api_version >= 5:
            self.channels = {}
            for list_id in self.channel_lists:
                r = await self.getChannelList(list_id)
                if r:
                    for channel in r:
                        self.channels[str(channel['ccid'])] = channel
                return r
        else:
            r = cast(Optional[ChannelsType], await self._getReq('channels'))
            if r:
                self.channels = r
            else:
                self.channels = {}
            return r

    async def getChannelId(self):
        if self.api_version >= 5:
            r = cast(Optional[ActivitesTVType], await self._getReq('activities/tv'))
        else:
            r = cast(Optional[ChannelsCurrentType], await self._getReq('channels/current'))

        self.channel = r
        return r

    async def getChannelName(self, ccid) -> Optional[str]:
        if not self.channels:
            return None
        return self.channels.get(ccid, dict()).get('name', None)

    async def getChannelLogo(self, ccid, channel_list="all") -> Tuple[Optional[bytes], Optional[str]]:
        if self.api_version >= 5:
            data, content_type = await self._getBinary(f"channeldb/tv/channelLists/{channel_list}/{ccid}/logo")
        else:
            data, content_type = await self._getBinary(f"channels/{ccid}/logo.png")
        return data, content_type

    async def getContext(self) -> Optional[ContextType]:
        if self.api_version >= 5:
            r = cast(Optional[ContextType], await self._getReq(f"context"))
            self.context = r
            return r

    async def setChannel(self, ccid, list_id: str = "alltv"):
        channel: Union[ActivitesTVType, ChannelsCurrentType]
        if self.api_version >= 5:
            channel = {"channelList": {"id": list_id}, "channel": {"ccid": ccid}}
            if await self._postReq('activities/tv', cast(Dict, channel)) is not None:
                self.channel = channel
        else:
            channel = {'id': ccid}
            if await self._postReq('channels/current', cast(Dict, channel)) is not None:
                self.channel = channel

    async def getChannelLists(self):
        if self.api_version >= 5:
            r = cast(ChannelDbTv, await self._getReq('channeldb/tv'))
            if r:
                self.channel_lists = {
                    data["id"]: data
                    for data in r.get("channelLists", {})
                }
                self.favorite_lists = {
                    data["id"]: data
                    for data in r.get("favoriteLists", {})
                }
            else:
                self.channel_lists = {}
                self.favorite_lists = {}
            return r

    async def getFavoriteList(self, list_id: str):
        if self.api_version >= 5:
            r = cast(Optional[FavoriteListType], await self._getReq(
                f"channeldb/tv/favoriteLists/{list_id}"
            ))
            return r["channels"]

    async def getChannelList(self, list_id: str):
        if self.api_version >= 5:
            r = cast(Optional[ChannelListType], await self._getReq(
                f"channeldb/tv/channelLists/{list_id}"
            ))
            return r["Channel"]

    async def getSources(self):
        if self.json_feature_supported("activities", "intent"):
            self.sources = {
                channel_uri(None): {
                    "name": "Watch TV"
                },
                passthrough_uri("com.mediatek.tvinput/.hdmi.HDMIInputService/HW5") : {
                    "name": "HDMI 1"
                },
                passthrough_uri("com.mediatek.tvinput/.hdmi.HDMIInputService/HW6") : {
                    "name": "HDMI 2"
                },
                passthrough_uri("com.mediatek.tvinput/.hdmi.HDMIInputService/HW7") : {
                    "name": "HDMI 3"
                },
                passthrough_uri("com.mediatek.tvinput/.hdmi.HDMIInputService/HW8") : {
                    "name": "HDMI 4"
                },
            }
            return self.sources

        if self.api_version == 1:
            r = await self._getReq('sources')
            if r:
                self.sources = r
            else:
                self.sources = {}
            return r

    async def getSourceId(self):
        if self.api_version < 5:
            r = await self._getReq('sources/current')
            if r:
                self.source_id = r['id']
            else:
                self.source_id = None
            return r

    async def getSourceName(self, srcid) -> Optional[str]:
        if not self.sources:
            return None
        return self.sources.get(srcid, dict()).get('name', None)

    async def setSource(self, source_id):
        if self.api_version == 1:
            r = await self._postReq('sources/current', {'id': source_id}) 
            if r is not None:
                return True
            return False

        if self.json_feature_supported("activities", "intent"):
            if source_id == CHANNEL_URI and self.channel_id:
                source_id = channel_uri(self.channel_id)

            intent: ApplicationIntentType = {
                "extras": {"uri": source_id},
                "action": "org.droidtv.playtv.SELECTURI", 
                "component": {
                    "packageName":"org.droidtv.playtv",
                    "className":"org.droidtv.playtv.PlayTvActivity"
                }
            }
            return await self.setApplication(intent)

        return False

    async def getApplications(self):
        if self.json_feature_supported("applications", None):
            r = cast(ApplicationsType, await self._getReq('applications'))
            if r:
                self.applications = {
                    app["id"]: app
                    for app in r["applications"]
                }
            else:
                self.applications = {}
            return r

    async def getApplication(self):
        if self.json_feature_supported("applications", None):
            r = cast(ApplicationIntentType, await self._getReq('activities/current'))
            if r:
                self.application = r
            else:
                self.application = None
            return r

    async def getApplicationIcon(self, id) -> Tuple[Optional[bytes], Optional[str]]:
        if self.json_feature_supported("applications", None):
            data, content_type = await self._getBinary(f"applications/{id}/icon")
            return data, content_type
        else:
            return None, None

    async def getPowerState(self):
        if self.api_version >= 5:
            r = await self._getReq('powerstate')
            if r:
                self.powerstate = cast(str, r["powerstate"])
            else:
                self.powerstate = None
            return r
        else:
            self.powerstate = None

    async def setPowerState(self, state):
        if self.api_version >= 5:
            data = {
                "powerstate": state
            }
            if await self._postReq('powerstate', data) is not None:
                self.powerstate = state
                return True
        return False

    async def getScreenState(self):
        if self.api_version >= 5:
            r = await self._getReq('screenstate')
            if r:
                self.screenstate = cast(str, r["screenstate"])
            else:
                self.screenstate = None
            return r
        else:
            self.screenstate = None

    async def setScreenState(self, state):
        if self.api_version >= 5:
            data = {
                "screenstate": state
            }
            if await self._postReq('screenstate', data) is not None:
                self.screenstate = state
                return True
        return False
    
    async def setApplication(self, intent: ApplicationIntentType):
        if self.json_feature_supported("activities", "intent"):
            data = {
                "intent": intent
            }
            if await self._postReq('activities/launch', data) is not None:
                self.application = intent
                return True
        return False

    async def setVolume(self, level, muted=False):
        data = {}
        if level is not None:
            if self.min_volume is None or self.max_volume is None:
                await self.getAudiodata()
            assert(self.max_volume is not None)
            assert(self.min_volume is not None)

            try:
                targetlevel = int(level * self.max_volume)
            except ValueError:
                LOG.warning("Invalid audio level %s" % str(level))
                return False
            if targetlevel < self.min_volume or targetlevel > self.max_volume:
                LOG.warning("Level not in range (%i - %i)" % (self.min_volume, self.max_volume))
                return False
            data['current'] = targetlevel

        data['muted'] = muted

        if await self._postReq('audio/volume', data) is None:
            return False

        self.audio_volume.update(data)

    async def sendKey(self, key):
        res = await self._postReq('input/key', {'key': key}) is not None
        if res:
            if key == "Mute":
                if self.audio_volume:
                    self.audio_volume["muted"] = not self.audio_volume["muted"]
            elif key == "VolumeUp":
                if self.audio_volume and self.audio_volume["current"] < self.audio_volume["max"]:
                    self.audio_volume["current"] += 1
            elif key == "VolumeDown":
                if self.audio_volume and self.audio_volume["current"] > self.audio_volume["min"]:
                    self.audio_volume["current"] -= 1

    async def sendUnicode(self, key: str):
        return await self._postReq('input/key', {'unicode': key}) is not None

    async def getAmbilightMode(self):
        data = await self._getReq('ambilight/mode')
        if data:
            self.ambilight_mode = data["current"]
            return data["current"]
        else:
            self.ambilight_mode = None

    async def setAmbilightMode(self, mode):
        data = {
            "current": mode
        }
        if await self._postReq('ambilight/mode', data) is None:
            return False
        self.ambilight_mode = mode
        return True

    async def getAmbilightTopology(self):
        r = await self._getReq('ambilight/topology')
        if r:
            self.ambilight_topology = r
        else:
            self.ambilight_topology = None
        return r

    async def getAmbilightMeasured(self):
        r = await self._getReq('ambilight/measured')
        if r:
            self.ambilight_measured = r
        else:
            self.ambilight_measured = None
        return r

    async def getAmbilightProcessed(self):
        r = await self._getReq('ambilight/processed')
        if r:
            self.ambilight_processed = r
        else:
            self.ambilight_processed = None
        return r

    async def getAmbilightCached(self):
        r = await self._getReq('ambilight/cached')
        if r:
            self.ambilight_cached = r
        else:
            self.ambilight_cached = None
        return r

    async def setAmbilightCached(self, data):
        if await self._postReq('ambilight/cached', data) is None:
            return False
        self.ambilight_cached = data
        return True

    async def openURL(self, url):
        if self.json_feature_supported("activities", "browser"):
            r = await self._postReq('activities/browser', {'url': url})
            return r is not None

    async def notifyChange(self, timeout = TIMEOUT_NOTIFYREAD):
        """Start a http connection waiting for changes."""
        if not self.notify_change_supported:
            return None

        data = {
            "notification": {
                "activities/tv": self.channel,
                "activities/current": self.application,
                "powerstate": {"powerstate": self.powerstate},
                "audio/volume": self.audio_volume,
                "context": self.context,
                "screenstate": {"screenstate": self.screenstate},
            }
        }

        timeout_ctx = httpx.Timeout(timeout=TIMEOUT, pool=TIMEOUT_POOL, read=timeout)
        try:
            result = await self._postReq('notifychange', data=data, timeout=timeout_ctx)
        except ProtocolFailure as err:
            # not uncommon for tv to close connection on the lingering connection
            LOG.debug("Protocol failure from device: %s", repr(err))
            result = None
        except ConnectionFailure as err:
            LOG.debug("Connection failure to device: %s", repr(err))
            self.on = False
            result = None

        if result:
            if "activities/tv" in result:
                self.channel = result["activities/tv"]

            if "activities/current" in result:
                self.application = result["activities/current"]

            if "powerstate" in result:
                self.powerstate = result["powerstate"]["powerstate"]

            if "audio/volume" in result:
                self.audio_volume = result["audio/volume"]

            if "context" in result:
                self.context = result["context"]

            if "screenstate" in result:
                self.screenstate = result["screenstate"]["screenstate"]
            return True
        else:
            return False
