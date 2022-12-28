import os
from time import sleep

from lib.ableton.interface.interface_color_enum import InterfaceColorEnum
from lib.ableton.interface.track import get_track_coords
from lib.ableton_set import AbletonSet
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import drag_to, keep_mouse_position, click
from lib.process import kill_window_by_criteria


def _assert_load_matching_track_conditions(set: AbletonSet) -> None:
    if set.current_track_type != "SimpleAudioTrack":
        raise Protocol0Error(f"Invalid track type: {set.current_track_type}")
    try:
        set.current_track_index_in_tracks
    except IndexError:
        raise Protocol0Error("Track is not a set saved track")


@keep_mouse_position
def load_matching_track(set: AbletonSet):
    _assert_load_matching_track_conditions(set)

    coords = get_track_coords(InterfaceColorEnum.TRACK_FOCUSED)

    os.startfile(set.tracks_folder)
    # sleep(0.5)

    index = set.current_track_index_in_tracks
    row_index = index // 2
    # using Small icons explorer display
    x = 740
    if index % 2 != 0:
        x += 385

    click(x, 377 + row_index * 40, keep_position=False)  # place cursor on track
    sleep(0.5)
    drag_to(*coords, duration=0.2)

    # remove the explorer window
    kill_window_by_criteria(name="tracks")
