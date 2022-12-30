from api.client.p0_script_api_client import p0_script_client
from lib.ableton.interface.pixel import get_color_coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton.track_folder import TrackFolder, ExplorerDisplayEnum
from lib.ableton_set import AbletonSet
from lib.mouse.mouse import drag_to, keep_mouse_position
from lib.process import kill_window_by_criteria
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def drag_matching_track(set: AbletonSet):
    track_folder = TrackFolder(set.tracks_folder, ExplorerDisplayEnum.SMALL_ICONS)
    track_folder.click_track(set.current_track_name)

    drag_to(get_color_coords(PixelColorEnum.TRACK_FOCUSED), duration=0.2)

    # remove the explorer window
    kill_window_by_criteria(name="tracks")
    p0_script_client().dispatch(EmitBackendEventCommand("matching_track_loaded"))
