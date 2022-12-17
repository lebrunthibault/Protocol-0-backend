import os
import time
from os.path import basename
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
from protocol0.application.command.DeleteSelectedTrackCommand import DeleteSelectedTrackCommand


def load_matching_track(set: AbletonSet):
    if set.current_track_type != "SimpleAudioTrack":
        notification_window.delay(
            f"Invalid track type: {set.current_track_type}",
            notification_enum=NotificationEnum.WARNING.value,
        )
        return

    tracks = [basename(t).replace(".als", "") for t in set.saved_tracks]

    if set.current_track_name not in tracks:
        notification_window.delay(
            "Track is not a set saved track", notification_enum=NotificationEnum.WARNING.value
        )
        return

    if not is_browser_visible():
        notification_window.delay(
            "Reselect your track", notification_enum=NotificationEnum.WARNING.value, centered=True
        )
        return

    preload_set_tracks(set)

    track_index = tracks.index(set.current_track_name)
    x_orig, y_orig = pyautogui.position()

    move_to(290, 156 + track_index * 24)  # place cursor on track
    # slight offset to have the subtrack be inserted at the left
    drag_duration = 0.5

    # in grouped track live interface reacts more slower
    if set.current_track_is_grouped:
        drag_duration = 2

    drag_to(x_orig, y_orig, duration=drag_duration)


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

    browser_visible = is_browser_visible()

    if not browser_visible:
        notification_window.delay(
            "Reselect your track", notification_enum=NotificationEnum.WARNING.value, centered=True
        )

    preload_set_tracks(set)

    if not browser_visible:
        return

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
    sleep(1.5)
    saved_track = set.last_saved_track
    saved_track_name = basename(saved_track).replace(".als", "")

    if (
        saved_track_name != set.current_track_name
        or time.time() - os.path.getatime(saved_track) > 2
    ):
        notification_window.delay(
            "Track was not saved",
            notification_enum=NotificationEnum.ERROR.value,
            centered=True,
        )
        return
    else:
        p0_script_client_from_http().dispatch(DeleteSelectedTrackCommand(set.current_track_name))
        notification_window.delay("Saved", notification_enum=NotificationEnum.SUCCESS.value)
