""" websocket endpoint for broadcasting the song state """
import json
from typing import List

from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from api.http_server.db import SongState, DB
from lib.song_state import SongStateManager

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

        if DB.song_state is not None:
            await self.broadcast_song_state(DB.song_state)

        await self.broadcast_sever_state()

    def disconnect(self, websocket: WebSocket):
        self._active_connections.remove(websocket)

    async def broadcast_song_state(self, song_state: SongState):
        for connection in self._active_connections:
            await connection.send_text(
                json.dumps({"type": "SONG_STATE", "data": song_state.dict()})
            )

        await ws_manager.broadcast_sever_state()

    async def broadcast_sever_state(self):
        song_states = list(
            sorted([ss.dict() for ss in SongStateManager.all()], key=lambda s: s["title"])
        )
        server_state = {"song_states": song_states}

        for connection in self._active_connections:
            await connection.send_text(json.dumps({"type": "SERVER_STATE", "data": server_state}))


ws_manager = ConnectionManager()


@ws_router.get("/ws/connections")
async def get_connections():
    return [ws.client for ws in ws_manager.active_connections]


@ws_router.websocket("/song_state")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            if _DEBUG:
                logger.info(f"Received song state data: {data}")
    except WebSocketDisconnect:
        pass

    ws_manager.disconnect(websocket)
