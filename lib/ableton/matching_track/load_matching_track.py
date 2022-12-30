import os
from time import sleep

from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)
from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.interface.pixel import get_color_coords, get_absolute_coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton_set import AbletonSet
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import drag_to, keep_mouse_position, click
from lib.process import kill_window_by_criteria
from lib.window.window import focus_window


def _assert_load_matching_track_conditions(set: AbletonSet) -> None:
    try:
        set.current_track_index_in_tracks
    except (IndexError, ValueError):
        raise Protocol0Error("Track is not a set saved track")


@keep_mouse_position
def drag_matching_track(set: AbletonSet):
    _assert_load_matching_track_conditions(set)

    coords = get_color_coords(PixelColorEnum.TRACK_FOCUSED)

    os.startfile(set.tracks_folder)
    handle = retry(10, 0.1)(focus_window)(name=Settings().track_window_title)

    index = set.current_track_index_in_tracks
    row_index = index // 2
    # using Small icons explorer display
    x = 340
    if index % 2 != 0:
        x += 385

    # place cursor on track
    click(
        *get_absolute_coords(handle, (x, 200 + row_index * 40)),
        exact=True,
    )
    sleep(0.5)
    drag_to(coords, duration=0.2)

    # remove the explorer window
    kill_window_by_criteria(name="tracks")
    p0_script_client().dispatch(EmitBackendEventCommand("matching_track_loaded"))
