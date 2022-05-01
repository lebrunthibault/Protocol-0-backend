from typing import Optional

from fastapi import APIRouter
from loguru import logger
from protocol0.application.command.DrumRackToSimplerCommand import DrumRackToSimplerCommand
from protocol0.application.command.FireSceneToPositionCommand import FireSceneToPositionCommand
from protocol0.application.command.LoadDeviceCommand import LoadDeviceCommand
from protocol0.application.command.LoadDrumRackCommand import LoadDrumRackCommand
from protocol0.application.command.LoadDrumTrackCommand import LoadDrumTrackCommand
from protocol0.application.command.ScrollScenePositionCommand import ScrollScenePositionCommand
from protocol0.application.command.ScrollSceneTracksCommand import ScrollSceneTracksCommand
from protocol0.application.command.SelectOrLoadDeviceCommand import SelectOrLoadDeviceCommand
from protocol0.application.command.ToggleArmCommand import ToggleArmCommand
from protocol0.application.command.ToggleDrumsCommand import ToggleDrumsCommand
from protocol0.application.command.ToggleRoomEQCommand import ToggleRoomEQCommand
from protocol0.application.command.ToggleSceneLoopCommand import ToggleSceneLoopCommand
from protocol0.application.command.ToggleTrackCommand import ToggleTrackCommand

from api.http_server.db import SongState, DB
from api.http_server.ws import ws_manager
from api.midi_server.p0_backend_api_client import dispatch_to_script, backend_client
from config import Config
from lib.desktop.desktop import go_to_desktop
from lib.process import execute_python_script_in_new_window, execute_process_in_new_window

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/reload_ableton")
async def reload_ableton():
    backend_client.reload_ableton()


@router.get("/song_state")
async def song_state() -> Optional[SongState]:
    return DB.SONG_STATE


@router.post("/song_state")
async def post_song_state(song_state: SongState):
    logger.info(f"received http {song_state}")
    DB.SONG_STATE = song_state
    await ws_manager.broadcast_song_state(song_state)


@router.get("/save_set_as_template")
async def save_set_as_template():
    backend_client.save_set_as_template()


@router.get("/tail_logs")
async def tail_logs():
    execute_python_script_in_new_window(f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py")


@router.get("/tail_logs_raw")
async def tail_logs_raw():
    execute_python_script_in_new_window(f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py", "--raw")


@router.get("/open_ableton")
async def open_ableton():
    go_to_desktop(0)
    execute_process_in_new_window(f"& \"{Config.ABLETON_EXE}\"")


@router.get("/open_current_set")
async def open_current_set():
    go_to_desktop(0)
    execute_process_in_new_window(f"& \"{Config.ABLETON_CURRENT_SET}\"")


@router.get("/open_default_set")
async def open_default_set():
    go_to_desktop(0)
    execute_process_in_new_window(f"& \"{Config.ABLETON_DEFAULT_SET}\"")


@router.get("/toggle_room_eq")
async def toggle_room_eq():
    dispatch_to_script(ToggleRoomEQCommand())


@router.get("/load_device/{name}")
async def load_device(name: str):
    dispatch_to_script(LoadDeviceCommand(name))


@router.get("/select_or_load_device/{name}")
async def select_or_load_device(name: str):
    dispatch_to_script(SelectOrLoadDeviceCommand(name))


@router.get("/load_drum_track/{name}")
async def load_drum_track(name: str):
    dispatch_to_script(LoadDrumTrackCommand(name))


@router.get("/load_drum_rack/{name}")
async def load_drum_rack(name: str):
    dispatch_to_script(LoadDrumRackCommand(name))


@router.get("/drum_rack_to_simpler")
async def drum_rack_to_simpler():
    dispatch_to_script(DrumRackToSimplerCommand())


@router.get("/arm")
async def arm():
    dispatch_to_script(ToggleArmCommand())


@router.get("/toggle_scene_loop")
async def toggle_scene_loop():
    dispatch_to_script(ToggleSceneLoopCommand())


@router.get("/fire_scene_to_position/{bar_length}")
@router.get("/fire_scene_to_position")
async def fire_scene_to_position(bar_length: Optional[int] = None):
    dispatch_to_script(FireSceneToPositionCommand(bar_length))


@router.get("/scroll_scene_position/{direction}")
async def scroll_scene_position(direction: str):
    dispatch_to_script(ScrollScenePositionCommand(go_next=direction == "right"))


@router.get("/scroll_scene_tracks/{direction}")
async def scroll_scene_tracks(direction: str):
    dispatch_to_script(ScrollSceneTracksCommand(go_next=direction == "right"))


@router.get("/toggle_track/{name}")
async def toggle_track(name: str):
    dispatch_to_script(ToggleTrackCommand(name))


@router.get("/toggle_drums")
async def toggle_drums():
    dispatch_to_script(ToggleDrumsCommand())
