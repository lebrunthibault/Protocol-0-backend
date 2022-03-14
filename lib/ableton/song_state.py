import asyncio
import json
from typing import List, Dict

import requests
import websockets

from config import Config


class SongState():
    def __init__(self):
        self._track_names: List[str] = []

    def to_dict(self):
        return {
            "track_names": self._track_names
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @property
    def track_names(self) -> List[str]:
        return self._track_names

    def update(self, state: Dict):
        self._track_names = state["track_names"]
        self._notify_http()
        asyncio.run(self._notify_stream_deck())

    def _notify_http(self):
        requests.post(f"{Config.HTTP_API_URL}/song_state", data=self.to_json())

    async def _notify_stream_deck(self):
        async with websockets.connect(f"ws://localhost:{Config.WS_PORT}") as websocket:
            # await websocket.send("from song state")
            await websocket.send(self.to_json())
            # await websocket.recv()
            await websocket.close()

