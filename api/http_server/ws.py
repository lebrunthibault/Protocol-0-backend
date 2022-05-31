""" websocket endpoint for broadcasting the song state """
from typing import List

from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.http_server.db import SongState, DB

ws_router = APIRouter()

_DEBUG = False


class ConnectionManager:

    def __init__(self):
        self._active_connections: List[WebSocket] = []

    def __repr__(self) -> str:
        return f"{len(self._active_connections)} active connections"

    @property
    def active_connections(self) -> List[WebSocket]:
        return self._active_connections

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._active_connections.append(websocket)
        if _DEBUG:
            logger.info(f"connection added: {self}")

    def disconnect(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def broadcast_song_state(self, song_state: SongState):
        if _DEBUG:
            logger.info(f"sending song state: {self}")
        for connection in self._active_connections:
            await connection.send_text(song_state.json())


ws_manager = ConnectionManager()


@ws_router.get("/ws/connections")
async def get_connections():
    return [ws.client for ws in ws_manager.active_connections]


@ws_router.websocket("/song_state")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    if DB.song_state:
        await websocket.send_text(DB.song_state.json())

    try:
        while True:
            data = await websocket.receive_text()
            if _DEBUG:
                logger.info(f"Received song state data: {data}")
    except WebSocketDisconnect:
        pass

    ws_manager.disconnect(websocket)
