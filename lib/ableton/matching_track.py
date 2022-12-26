import os
from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client_from_http
from gui.celery import notification_window
from lib.ableton.ableton import is_browser_visible, is_browser_tracks_folder_clickable
from lib.ableton.browser import preload_set_tracks
from lib.ableton_set import AbletonSet
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.keys import send_keys, send_left
from lib.mouse.mouse import drag_to, move_to, keep_mouse_position, click
from lib.process import kill_window_by_criteria
from lib.screen import get_selected_track_header_coordinates, focus_left_most_track
from protocol0.application.command.DeleteSelectedTrackCommand import DeleteSelectedTrackCommand
from protocol0.application.command.SelectTrackCommand import SelectTrackCommand


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

    focus_left_most_track()
    p0_script_client_from_http().dispatch(SelectTrackCommand(set.current_track_name), log=True)
    sleep(0.1)
    coords = get_selected_track_header_coordinates()

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


def save_and_remove_matching_track(set: AbletonSet):
    if set.current_track_type not in ("ExternalSynthTrack", "SimpleMidiTrack"):
        raise Protocol0Error(f"Invalid track type: {set.current_track_type}")

    if not is_browser_tracks_folder_clickable():
        raise Protocol0Error("Browser is not selectable")

    if not is_browser_visible():
        raise Protocol0Error("Browser is not visible")

    preload_set_tracks(set)

    initial_mouse_position = pyautogui.position()

    # drag track to tracks
    drag_to(278, 156)

    sleep(0.5)
    # save
    send_keys("{ENTER}")
    send_left()
    send_keys("{ENTER}")

    move_to(*initial_mouse_position)

    # checking the track was saved
    sleep(1)

    if not set.is_track_saved:
        sleep(2)

        if not set.is_track_saved:
            raise Protocol0Error("Track was not saved")

    send_left()  # fold the set sub track
    p0_script_client_from_http().dispatch(DeleteSelectedTrackCommand(set.current_track_name))
    notification_window.delay("Saved", notification_enum=NotificationEnum.SUCCESS.value)
