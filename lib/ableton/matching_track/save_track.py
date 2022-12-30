import shutil
from time import sleep

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.interface.browser import preload_set_tracks, toggle_browser, is_browser_visible
from lib.ableton.interface.pixel import get_color_coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton_set import AbletonSet
from lib.decorators import retry
from lib.keys import send_keys
from lib.mouse.mouse import drag_to, keep_mouse_position, move_to
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@retry(10, 0)
def _wait_for_track_save(set: AbletonSet):
    sleep(0.1)
    assert set.is_current_track_saved, "Track not yet saved"


@retry(5, 0.1)
def _close_browser():
    toggle_browser()
    assert not is_browser_visible()


@keep_mouse_position
def save_track_to_sub_tracks(set: AbletonSet):
    preload_set_tracks(set)
    assert set.saved_temp_track is None, "No temp track should be saved"

    move_to(get_color_coords(PixelColorEnum.TRACK_FOCUSED))

    drag_to((234, 496), duration=0.3)  # drag to a free spot

    _wait_for_track_save(set)

    shutil.move(str(set.saved_temp_track), f"{set.tracks_folder}/{set.current_track_name}.als")

    send_keys("{ESC}")  # close the name prompt
    _close_browser()

    p0_script_client().dispatch(EmitBackendEventCommand("track_saved"))
