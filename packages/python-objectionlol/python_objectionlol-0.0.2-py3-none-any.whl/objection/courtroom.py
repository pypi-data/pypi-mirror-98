import logging
import asyncio
import json
import time

from urllib.parse import urlencode

import aiohttp

from .utils import make_data, clear_json
from .types.events import parse_event
from .handlers import Handlers

log = logging.getLogger("client")


class CourtRoom(Handlers):
    BASE_URL = "courtroom.objection.lol:9005"
    SOCKETIO_URL = f"{BASE_URL}/socket.io/"
    WS_SOCKETIO_URL = f"wss://{SOCKETIO_URL}"
    HTTPS_SOCKETIO_URL = f"https://{SOCKETIO_URL}"

    def __init__(self, courtroom_id):
        self.courtroom_id = courtroom_id
        # have to disable ssl verification
        # because it can't verify objection.lol certs
        connector = aiohttp.TCPConnector(ssl=False)
        self.aiohttp_cs = aiohttp.ClientSession(
            connector=connector)

        self.handlers = dict()

        self.closed = False
        self._ready = False

    @property
    def polling_params(self):
        return self.get_params("polling")

    @property
    def websocket_params(self):
        return self.get_params("websocket")

    def get_params(self, transport):
        params = {
            "EIO": 3,
            "transport": transport
        }
        if hasattr(self, "sid"):
            params["sid"] = self.sid
        params["t"] = str(time.time())
        return params

    def is_connected(self):
        connected = hasattr(self, "ws") and not self.ws.closed
        log.debug(
            f"connected: {connected}; hasattr: {hasattr(self, 'ws')};"
            f" closed: {self.ws.closed if hasattr(self, 'ws') else False}"
        )
        return connected

    async def probe_room(self):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")

        await self.ws.send_str("2probe")
        async with self.aiohttp_cs.get(self.HTTPS_SOCKETIO_URL,
                                       params=self.polling_params) as r:
            await r.text()

        req = ["probe_room", self.courtroom_id]
        data = make_data("25:42", req)

        async with self.aiohttp_cs.post(self.HTTPS_SOCKETIO_URL,
                                        data=data,
                                        params=self.polling_params) as r:
            return await r.text()

    async def join_room(self, username, password=""):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")

        req = ["join_room", {"username": username, "password": password}]
        data = make_data("42", req)
        self.username = username
        await self.ws.send_str(data)

    async def send_plain_message(self, text):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")

        req = ["plain_message", text]
        data = make_data("42", req)
        await self.ws.send_str(data)

    async def send_message(self, text, pose_id=1, bubble_type=1,
                           merge_next=False, do_not_talk=False,
                           go_next=False, pose_animation=True,
                           flipped=False,
                           frame_actions=[], frame_fades=[],
                           background=None, character_id=None,
                           popup_id=None,
                           username=None):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")
        req = ["message",
               {
                   "id": -1,
                   "text": text,
                   "poseId": pose_id,
                   "bubbleType": bubble_type,
                   "username": username or self.username,
                   "mergeNext": merge_next,
                   "doNotTalk": do_not_talk,
                   "goNext": go_next,
                   "poseAnimation": pose_animation,
                   "flipped": flipped,
                   "frameActions": frame_actions,
                   "frameFades": frame_fades,
                   "background": background,
                   "characterId": character_id,
                   "popupId": popup_id
               }
               ]
        data = make_data("42", req)
        await self.ws.send_str(data)

    async def get_socketio(self):
        if self.closed:
            raise RuntimeError("client is closed")
        async with self.aiohttp_cs.get(self.HTTPS_SOCKETIO_URL,
                                       params=self.polling_params) as r:
            data = await r.text()
        data = clear_json(data)
        data = json.loads(data)

        self.sid = data["sid"]
        self.ping_interval = data["pingInterval"] // 1000
        return data

    async def _heartbeat(self):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")

        while not self._ready:
            await asyncio.sleep(0)

        await self.ws.send_str("2")
        if self.handlers.get("start"):
            await self.handlers["start"]()
            log.info("started")

        while self.is_connected() and not self.closed:
            await asyncio.sleep(self.ping_interval)
            await self.ws.send_str("2")
            log.debug("sent 2!")

    async def _ws_loop(self):
        if not self.is_connected():
            raise RuntimeError("websocket is not connected")
        if self.closed:
            raise RuntimeError("client is closed")

        ws = self.ws
        while not ws.closed and not self.closed:
            async for msg in ws:
                log.debug(f"received {msg.type} with {msg.data}")
                if msg.type == aiohttp.WSMsgType.ERROR:
                    log.error("received error with {msg.data}, stopping")
                    break
                elif msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == "3probe":
                        log.debug("sent 5!")
                        self._ready = True
                        await ws.send_str("5")
                    elif msg.data.startswith("42"):
                        data = json.loads(clear_json(msg.data))
                        event = data[0]
                        data = data[1]
                        log.debug(f"received {data}")

                        data = parse_event(event, data)
                        if event == "room_data":
                            self.users = data.users
                            self.pairs = data.pairs

                            self.background = data.background
                            self.evidence = data.background

                            self.title = data.title
                            self.permissions = data.permissions
                        elif event == "join_success":
                            self.user = data.user
                        if self.handlers.get(event):
                            log.debug(f"triggered {event}")
                            await self.handlers[event](data)
                        elif event == "critical_error":
                            await self.close()
                            break
                elif msg.type == aiohttp.WSMsgType.CLOSE:
                    log.info(f"connection closed with {msg.data}")

    def wait(self):
        return self.ws_task

    async def start(self):
        if self.closed:
            raise RuntimeError("client is closed")
        await self.get_socketio()

        params = urlencode(self.websocket_params)
        url = self.WS_SOCKETIO_URL + "?" + params
        self.ws_task = asyncio.create_task(self._start(url))

    async def _start(self, url):
        async with self.aiohttp_cs.ws_connect(
                url) as ws:
            self.ws = ws

            await self.probe_room()
            self._heartbeat_task = asyncio.create_task(self._heartbeat())
            try:
                await asyncio.gather(self._ws_loop(), self._heartbeat_task)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logging.error(e, exc_info=True)

        if self.handlers.get("stop"):
            await self.handlers["stop"]()
        log.info("ws disconnected")
        delattr(self, "ws")

    async def close(self):
        if self.is_connected():
            await self.ws.close()
        await self.aiohttp_cs.close()
        if hasattr(self, "_heartbeat_task"):
            self._heartbeat_task.cancel()
        self.closed = True
