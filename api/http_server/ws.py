""" websocket endpoint for broadcasting the song state """
from typing import List

from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket

from api.http_server.db import SongState, DB

ws_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self._active_connections: List[WebSocket] = []

    def __repr__(self) -> str:
        return f"{len(self._active_connections)} active connections"

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active_connections.append(websocket)
        logger.info(f"connection added: {self}")

    def disconnect(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def broadcast_song_state(self, song_state: SongState):
        logger.info(f"sending song state: {self}")
        for connection in self._active_connections:
            await connection.send_text(song_state.json())


ws_manager = ConnectionManager()


@ws_router.websocket("/song_state")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    if DB.SONG_STATE:
        websocket.send_text(DB.SONG_STATE.json())

    while True:
        data = await websocket.receive_text()
        logger.info(f"Received {data}")
