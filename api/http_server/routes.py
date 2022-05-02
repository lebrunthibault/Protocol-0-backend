import time
from typing import Optional

from fastapi import APIRouter
from loguru import logger

from api.client.p0_script_api_client import p0_script_client_from_http
from api.http_server.db import SongState, DB
from api.http_server.ws import ws_manager
from config import Config
from lib.ableton.ableton import is_ableton_up, reload_ableton, save_set_as_template
from lib.desktop.desktop import go_to_desktop
from lib.process import execute_python_script_in_new_window, execute_process_in_new_window
from protocol0.application.command.DrumRackToSimplerCommand import DrumRackToSimplerCommand
from protocol0.application.command.FireSceneToPositionCommand import FireSceneToPositionCommand
from protocol0.application.command.LoadDeviceCommand import LoadDeviceCommand
from protocol0.application.command.LoadDrumRackCommand import LoadDrumRackCommand
from protocol0.application.command.LoadDrumTrackCommand import LoadDrumTrackCommand
from protocol0.application.command.ScrollScenePositionCommand import ScrollScenePositionCommand
from protocol0.application.command.ScrollSceneTracksCommand import ScrollSceneTracksCommand
from protocol0.application.command.ScrollScenesCommand import ScrollScenesCommand
from protocol0.application.command.SelectOrLoadDeviceCommand import SelectOrLoadDeviceCommand
from protocol0.application.command.ToggleArmCommand import ToggleArmCommand
from protocol0.application.command.ToggleDrumsCommand import ToggleDrumsCommand
from protocol0.application.command.ToggleRoomEQCommand import ToggleRoomEQCommand
from protocol0.application.command.ToggleSceneLoopCommand import ToggleSceneLoopCommand
from protocol0.application.command.ToggleTrackCommand import ToggleTrackCommand

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello World"}


@router.get("/reload_ableton")
async def _reload_ableton():
    reload_ableton()


@router.get("/song_state")
async def song_state() -> Optional[SongState]:
    return DB.SONG_STATE


@router.post("/song_state")
async def post_song_state(song_state: SongState):
    logger.info(f"received http {song_state}")
    DB.SONG_STATE = song_state
    await ws_manager.broadcast_song_state(song_state)


@router.get("/save_set_as_template")
async def _save_set_as_template():
    save_set_as_template()


@router.get("/tail_logs")
async def tail_logs():
    execute_python_script_in_new_window(f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py")


@router.get("/tail_logs_raw")
async def tail_logs_raw():
    execute_python_script_in_new_window(f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py", "--raw")


@router.get("/open_ableton")
async def open_ableton():
    go_to_desktop(0)

    if is_ableton_up():
        reload_ableton()
    else:
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
    p0_script_client_from_http.dispatch(ToggleRoomEQCommand())


@router.get("/load_device/{name}")
async def load_device(name: str):
    p0_script_client_from_http.dispatch(LoadDeviceCommand(name))


@router.get("/select_or_load_device/{name}")
async def select_or_load_device(name: str):
    p0_script_client_from_http.dispatch(SelectOrLoadDeviceCommand(name))


@router.get("/load_drum_track/{name}")
async def load_drum_track(name: str):
    p0_script_client_from_http.dispatch(LoadDrumTrackCommand(name))


@router.get("/load_drum_rack/{name}")
async def load_drum_rack(name: str):
    p0_script_client_from_http.dispatch(LoadDrumRackCommand(name))


@router.get("/drum_rack_to_simpler")
async def drum_rack_to_simpler():
    p0_script_client_from_http.dispatch(DrumRackToSimplerCommand())


@router.get("/arm")
async def arm():
    p0_script_client_from_http.dispatch(ToggleArmCommand())


@router.get("/toggle_scene_loop")
async def toggle_scene_loop():
    p0_script_client_from_http.dispatch(ToggleSceneLoopCommand())


@router.get("/fire_scene_to_position/{bar_length}")
@router.get("/fire_scene_to_position")
async def fire_scene_to_position(bar_length: Optional[int] = None):
    p0_script_client_from_http.dispatch(FireSceneToPositionCommand(bar_length))
    # p0_script_client_from_http.dispatch()(FireSceneToPositionCommand(bar_length))


@router.get("/scroll_scenes/{direction}")
async def scroll_scenes(direction: str):
    p0_script_client_from_http.dispatch(ScrollScenesCommand(go_next=direction == "down"))


@router.get("/scroll_scene_position/{direction}")
async def scroll_scene_position(direction: str):
    print(time.time())
    p0_script_client_from_http.dispatch(ScrollScenePositionCommand(go_next=direction == "right"))


@router.get("/scroll_scene_tracks/{direction}")
async def scroll_scene_tracks(direction: str):
    p0_script_client_from_http.dispatch(ScrollSceneTracksCommand(go_next=direction == "right"))


@router.get("/toggle_track/{name}")
async def toggle_track(name: str):
    p0_script_client_from_http.dispatch(ToggleTrackCommand(name))


@router.get("/toggle_drums")
async def toggle_drums():
    p0_script_client_from_http.dispatch(ToggleDrumsCommand())
