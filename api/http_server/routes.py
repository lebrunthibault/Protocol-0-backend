from typing import Optional

from fastapi import APIRouter
from loguru import logger
from protocol0.application.command.FireSceneToPositionCommand import FireSceneToPositionCommand
from protocol0.application.command.LoadDeviceCommand import LoadDeviceCommand
from protocol0.application.command.LoadDrumTrackCommand import LoadDrumTrackCommand
from protocol0.application.command.PlayPauseCommand import PlayPauseCommand
from protocol0.application.command.ToggleArmCommand import ToggleArmCommand
from protocol0.application.command.ToggleDrumsCommand import ToggleDrumsCommand
from protocol0.application.command.ToggleSceneLoopCommand import ToggleSceneLoopCommand
from protocol0.application.command.ToggleTrackCommand import ToggleTrackCommand

from api.http_server.db import SongState, DB
from api.http_server.ws import ws_manager
from api.midi_server.p0_backend_api_client import dispatch_to_script, backend_client
from config import Config
from lib.process import execute_in_new_window

router = APIRouter()


@router.get("/")
async def index():
    logger.info("in index")
    return {"message": "Hello World"}


@router.get("/reload_ableton")
async def reload_ableton():
    backend_client.reload_ableton()


@router.get("/song_state")
async def song_state() -> Optional[SongState]:
    return DB.SONG_STATE


@router.post("/song_state")
async def push_song_state(song_state: SongState):
    logger.info(f"received http {song_state}")
    DB.SONG_STATE = song_state
    await ws_manager.broadcast_song_state(song_state)


@router.get("/save_set_as_template")
async def save_set_as_template():
    backend_client.save_set_as_template()


@router.get("/tail_logs")
async def tail_logs():
    execute_in_new_window(f"{Config.PROJECT_ROOT}/scripts/tail_protocol0_logs.py")


@router.get("/tail_logs_raw")
async def tail_logs_raw():
    execute_in_new_window(f"{Config.PROJECT_ROOT}/scripts/tail_protocol0_logs.py", "--raw")


@router.get("/play_pause")
async def play_pause():
    dispatch_to_script(PlayPauseCommand())


@router.get("/load_device/{name}")
async def load_device(name: str):
    dispatch_to_script(LoadDeviceCommand(name))


@router.get("/load_drum_track/{name}")
async def load_device(name: str):
    dispatch_to_script(LoadDrumTrackCommand(name))


@router.get("/arm")
async def arm():
    dispatch_to_script(ToggleArmCommand())


@router.get("/toggle_scene_loop")
async def toggle_scene_loop():
    dispatch_to_script(ToggleSceneLoopCommand())


@router.get("/fire_scene_to_position")
async def fire_scene_to_position():
    dispatch_to_script(FireSceneToPositionCommand())


@router.get("/toggle_track/{name}")
async def toggle_track(name: str):
    dispatch_to_script(ToggleTrackCommand(name))


@router.get("/toggle_drums")
async def toggle_drums():
    dispatch_to_script(ToggleDrumsCommand())
