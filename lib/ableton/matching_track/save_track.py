import os
import shutil
from os.path import basename
from time import sleep

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.interface.browser import (
    toggle_browser,
    is_browser_visible,
    click_browser_tracks,
)
from lib.ableton.interface.coords import CoordsEnum
from lib.ableton.interface.track import get_focused_track_coords
from lib.ableton_set import AbletonSet, AbletonSetManager
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.keys import send_keys
from lib.mouse.mouse import drag_to, keep_mouse_position, move_to
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@retry(90, 0)  # 9 seconds max
def _wait_for_track_save(set: AbletonSet):
    sleep(0.1)
    assert set.is_current_track_saved, "Track not yet saved"


@retry(5, 0.1)
def _close_browser():
    toggle_browser()
    assert not is_browser_visible()


@keep_mouse_position
def save_track_to_sub_tracks(set: AbletonSet, check_for_duplicate: bool):
    assert len(AbletonSet.all_tracks_folder()) < 8, "Too many set tracks, drag cannot be made"
    if set.saved_temp_track is not None:
        os.unlink(set.saved_temp_track)

    if check_for_duplicate:
        if set.selected_track.name in [basename(t).split(".")[0] for t in set.saved_tracks]:
            os.startfile(AbletonSetManager.active().tracks_folder)
            raise Protocol0Error("Duplicate saved track")

    click_browser_tracks()

    # drag the track to the tracks folder
    move_to(get_focused_track_coords())
    drag_to(CoordsEnum.BROWSER_FREE_TRACK_SPOT.value, duration=0.3)  # drag to a free spot

    _wait_for_track_save(set)

    shutil.move(str(set.saved_temp_track), f"{set.tracks_folder}/{set.current_track.name}.als")

    sleep(0.1)
    send_keys("{ESC}")  # close the name prompt
    _close_browser()

    p0_script_client().dispatch(EmitBackendEventCommand("track_saved"))
