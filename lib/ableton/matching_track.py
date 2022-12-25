import os
from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client_from_http
from gui.celery import notification_window
from lib.ableton.ableton import is_browser_visible, is_browser_tracks_folder_clickable
from lib.ableton.browser import preload_set_tracks
from lib.ableton_set import AbletonSet
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys, send_left
from lib.mouse.mouse import drag_to, move_to
from lib.process import kill_window_by_criteria
from protocol0.application.command.DeleteSelectedTrackCommand import DeleteSelectedTrackCommand


def _assert_load_matching_track_conditions(set: AbletonSet) -> bool:
    if set.current_track_type != "SimpleAudioTrack":
        notification_window.delay(
            f"Invalid track type: {set.current_track_type}",
            notification_enum=NotificationEnum.WARNING.value,
        )
        return False

    try:
        set.current_track_index_in_tracks
    except IndexError:
        notification_window.delay(
            "Track is not a set saved track", notification_enum=NotificationEnum.WARNING.value
        )
        return False

    return True


def load_matching_track(set: AbletonSet):
    if not _assert_load_matching_track_conditions(set):
        return

    x_orig, y_orig = pyautogui.position()
    os.startfile(set.tracks_folder)
    sleep(0.5)

    index = set.current_track_index_in_tracks
    row_index = index // 2
    # using Small icons explorer display
    y = 850
    if index % 2 != 0:
        y = 1235

    move_to(y, 377 + row_index * 40)  # place cursor on track

    drag_to(x_orig, y_orig, duration=0.2)

    # remove the explorer window
    kill_window_by_criteria(name="tracks")


def load_matching_track_from_live(set: AbletonSet):
    if not _assert_load_matching_track_conditions(set):
        return

    if not is_browser_visible():
        notification_window.delay(
            "Browser is not visible",
            notification_enum=NotificationEnum.WARNING.value,
            centered=True,
        )
        return

    preload_set_tracks(set)

    x_orig, y_orig = pyautogui.position()

    move_to(290, 156 + set.current_track_index_in_tracks * 24)  # place cursor on track
    # slight offset to have the subtrack be inserted at the left

    drag_to(x_orig, y_orig)


def save_and_remove_matching_track(set: AbletonSet):
    if set.current_track_type not in ("ExternalSynthTrack", "SimpleMidiTrack"):
        notification_window.delay(
            f"Invalid track type: {set.current_track_type}",
            notification_enum=NotificationEnum.WARNING.value,
        )
        return

    if not is_browser_tracks_folder_clickable():
        notification_window.delay(
            "Browser is not selectable",
            notification_enum=NotificationEnum.WARNING.value,
            centered=True,
        )
        return

    if not is_browser_visible():
        notification_window.delay(
            "Browser is not visible",
            notification_enum=NotificationEnum.WARNING.value,
            centered=True,
        )
        return

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
            notification_window.delay(
                "Track was not saved",
                notification_enum=NotificationEnum.ERROR.value,
                centered=True,
            )
            return

    send_left()  # fold the set sub track
    p0_script_client_from_http().dispatch(DeleteSelectedTrackCommand(set.current_track_name))
    notification_window.delay("Saved", notification_enum=NotificationEnum.SUCCESS.value)
