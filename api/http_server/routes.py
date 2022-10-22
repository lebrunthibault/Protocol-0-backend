from typing import Optional

from fastapi import APIRouter

from api.client.p0_script_api_client import p0_script_client_from_http
from api.http_server.db import SongState, DB
from api.http_server.ws import ws_manager
from config import Config
from lib.ableton.ableton import (
    reload_ableton,
    save_set_as_template,
    open_set,
    toggle_clip_notes,
)
from lib.ableton.get_set import get_last_launched_set, get_kontakt_set
from lib.desktop.desktop import go_to_desktop
from lib.process import execute_python_script_in_new_window, execute_process_in_new_window
from lib.server_state import ServerState
from lib.song_state import SongStateManager
from protocol0.application.command.DrumRackToSimplerCommand import DrumRackToSimplerCommand
from protocol0.application.command.FireSceneToPositionCommand import FireSceneToPositionCommand
from protocol0.application.command.FireSelectedSceneCommand import FireSelectedSceneCommand
from protocol0.application.command.GoToGroupTrackCommand import GoToGroupTrackCommand
from protocol0.application.command.LoadDeviceCommand import LoadDeviceCommand
from protocol0.application.command.LoadDrumRackCommand import LoadDrumRackCommand
from protocol0.application.command.MuteSetCommand import MuteSetCommand
from protocol0.application.command.PlayPauseSongCommand import PlayPauseSongCommand
from protocol0.application.command.ReloadScriptCommand import ReloadScriptCommand
from protocol0.application.command.ScrollScenePositionCommand import ScrollScenePositionCommand
from protocol0.application.command.ScrollSceneTracksCommand import ScrollSceneTracksCommand
from protocol0.application.command.ScrollScenesCommand import ScrollScenesCommand
from protocol0.application.command.ScrollTrackVolumeCommand import ScrollTrackVolumeCommand
from protocol0.application.command.SelectOrLoadDeviceCommand import SelectOrLoadDeviceCommand
from protocol0.application.command.ShowAutomationCommand import ShowAutomationCommand
from protocol0.application.command.ShowInstrumentCommand import ShowInstrumentCommand
from protocol0.application.command.ToggleArmCommand import ToggleArmCommand
from protocol0.application.command.ToggleDrumsCommand import ToggleDrumsCommand
from protocol0.application.command.ToggleReferenceTrackCommand import ToggleReferenceTrackCommand
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


@router.get("/reload_script")
async def _reload_script():
    p0_script_client_from_http().dispatch(ReloadScriptCommand())


@router.get("/server_state")
async def server_state() -> ServerState:
    return ServerState.create()


@router.get("/song_state")
async def song_state() -> Optional[SongState]:
    return DB.song_state


@router.post("/song_state")
async def post_song_state(song_state: SongState):
    DB.song_state = song_state
    SongStateManager.register(song_state)
    await ws_manager.broadcast_song_state(song_state)


@router.delete("/set/{id}")
async def delete_set(id: str):
    SongStateManager.remove(id)
    DB.song_state = None
    await ws_manager.broadcast_sever_state()


@router.get("/save_set_as_template")
async def _save_set_as_template():
    save_set_as_template()


@router.get("/tail_logs")
async def tail_logs():
    execute_python_script_in_new_window(
        f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py"
    )


@router.get("/tail_logs_raw")
async def tail_logs_raw():
    execute_python_script_in_new_window(
        f"{Config.PROJECT_DIRECTORY}/scripts/tail_protocol0_logs.py", "--raw"
    )


@router.get("/open_ableton")
async def open_ableton():
    go_to_desktop(0)

    execute_process_in_new_window(f'& "{Config.ABLETON_EXE}"')


@router.get("/open_current_set")
async def open_current_set():
    open_set(Config.ABLETON_CURRENT_SET)


@router.get("/open_default_set")
async def open_default_set():
    open_set(Config.ABLETON_DEFAULT_SET)


@router.get("/open_last_set")
async def open_last_set():
    open_set(get_last_launched_set())


@router.get("/open_kontakt_set")
async def open_kontakt_set():
    open_set(get_kontakt_set())


@router.get("/mute_set/{set_id}")
async def mute_set(set_id: str):
    command = MuteSetCommand()
    song_state = SongStateManager.get(set_id)
    command.set_id = song_state.id

    p0_script_client_from_http().dispatch(command)


@router.get("/toggle_room_eq")
async def toggle_room_eq():
    p0_script_client_from_http().dispatch(ToggleRoomEQCommand())


@router.get("/play_pause")
async def play_pause():
    p0_script_client_from_http().dispatch(PlayPauseSongCommand())


@router.get("/load_device/{name}")
async def load_device(name: str):
    p0_script_client_from_http().dispatch(LoadDeviceCommand(name))


@router.get("/select_or_load_device/{name}")
async def select_or_load_device(name: str):
    p0_script_client_from_http().dispatch(SelectOrLoadDeviceCommand(name))


@router.get("/load_drum_rack/{category}/{subcategory}")
async def load_drum_rack(category: str, subcategory: str):
    p0_script_client_from_http().dispatch(LoadDrumRackCommand(category, subcategory))


@router.get("/drum_rack_to_simpler")
async def drum_rack_to_simpler():
    p0_script_client_from_http().dispatch(DrumRackToSimplerCommand())


@router.get("/arm")
async def arm():
    p0_script_client_from_http().dispatch(ToggleArmCommand())


@router.get("/toggle_scene_loop")
async def toggle_scene_loop():
    p0_script_client_from_http().dispatch(ToggleSceneLoopCommand())


@router.get("/fire_scene_to_position/{bar_length}")
@router.get("/fire_scene_to_position")
async def fire_scene_to_position(bar_length: Optional[int] = None):
    p0_script_client_from_http().dispatch(FireSceneToPositionCommand(bar_length))


@router.get("/fire_selected_scene")
async def fire_selected_scene():
    p0_script_client_from_http().dispatch(FireSelectedSceneCommand())


@router.get("/scroll_scenes/{direction}")
async def scroll_scenes(direction: str):
    p0_script_client_from_http().dispatch(ScrollScenesCommand(go_next=direction == "next"))


@router.get("/scroll_scene_position/{direction}")
async def scroll_scene_position(direction: str):
    p0_script_client_from_http().dispatch(ScrollScenePositionCommand(go_next=direction == "next"))


@router.get("/scroll_scene_position_fine/{direction}")
async def scroll_scene_position_fine(direction: str):
    p0_script_client_from_http().dispatch(
        ScrollScenePositionCommand(go_next=direction == "next", use_fine_scrolling=True)
    )


@router.get("/scroll_scene_tracks/{direction}")
async def scroll_scene_tracks(direction: str):
    p0_script_client_from_http().dispatch(ScrollSceneTracksCommand(go_next=direction == "next"))


@router.get("/scroll_track_volume/{direction}")
async def scroll_track_volume(direction: str):
    p0_script_client_from_http().dispatch(ScrollTrackVolumeCommand(go_next=direction == "next"))


@router.get("/toggle_track/{name}")
async def toggle_track(name: str):
    p0_script_client_from_http().dispatch(ToggleTrackCommand(name))


@router.get("/toggle_drums")
async def toggle_drums():
    p0_script_client_from_http().dispatch(ToggleDrumsCommand())


@router.get("/toggle_reference")
async def toggle_reference():
    p0_script_client_from_http().dispatch(ToggleReferenceTrackCommand())


@router.get("/show_instrument")
async def show_instrument():
    p0_script_client_from_http().dispatch(ShowInstrumentCommand())


@router.get("/show_automation/{direction}")
async def show_automation(direction: str):
    p0_script_client_from_http().dispatch(ShowAutomationCommand(go_next=direction == "next"))


@router.get("/toggle_clip_notes")
async def _toggle_clip_notes():
    toggle_clip_notes()


@router.get("/go_to_group_track")
async def _go_to_group_track():
    p0_script_client_from_http().dispatch(GoToGroupTrackCommand())
