import os
import time
from enum import Enum
from os.path import basename
from time import sleep
from typing import Tuple

import pyautogui
from loguru import logger

from api.client.p0_script_api_client import p0_script_client_from_http
from api.settings import Settings
from gui.celery import notification_window
from lib.ableton.ableton import show_plugins, is_browser_visible, is_browser_splurges_clickable
from lib.ableton.browser import preload_set_tracks
from lib.ableton_set import AbletonSet
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys, send_left
from lib.mouse.mouse import click, drag_to, move_to
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import get_window_position, focus_window
from protocol0.application.command.DeleteSelectedTrackCommand import DeleteSelectedTrackCommand

settings = Settings()


class Rev2ButtonsRelativeCoordinates(Enum):
    """These coordinates are relative to the plugin message == Mouse position relative from active_window.ahk"""

    # Relative coordinates
    ACTIVATION_MIDDLE_BUTTON = (784, 504)
    PROGRAM = (1067, 147)


def _get_absolute_button_position(
    handle: int, window_coordinates: Rev2ButtonsRelativeCoordinates
) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_button, y_button) = window_coordinates.value
    x_button *= settings.display_resolution_factor
    y_button *= settings.display_resolution_factor
    return (x + x_button, y + y_button)


def activate_rev2_editor():
    # type: () -> None
    _click_rev2_editor(Rev2ButtonsRelativeCoordinates.ACTIVATION_MIDDLE_BUTTON)


def post_activate_rev2_editor():
    # type: () -> None
    _click_rev2_editor(Rev2ButtonsRelativeCoordinates.PROGRAM)


def _click_rev2_editor(coordinates: Rev2ButtonsRelativeCoordinates):
    show_plugins()
    handle = find_window_handle_by_enum(settings.rev2_editor_window_title)
    if not handle:
        logger.warning(
            f"Couldn't find rev2 editor window for name: {settings.rev2_editor_window_title}. Check set naming"
        )
        return
    focus_window(name=settings.rev2_editor_window_title)
    click(
        *_get_absolute_button_position(handle, coordinates),
        exact=True,
    )


def load_ext_track(set: AbletonSet):
    if set.is_unknown:
        notification_window.delay(
            "Set is unknown", notification_enum=NotificationEnum.WARNING.value
        )
        return

    if set.current_track_type != "SimpleAudioTrack":
        notification_window.delay("Invalid track", notification_enum=NotificationEnum.WARNING.value)
        return

    tracks = [basename(t).replace(".als", "") for t in set.saved_tracks]

    if set.current_track_name not in tracks:
        notification_window.delay(
            "Track is not a set saved track", notification_enum=NotificationEnum.WARNING.value
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

    track_index = tracks.index(set.current_track_name)
    x_orig, y_orig = pyautogui.position()
    distance = track_index + 1
    if set.has_backup:
        distance += 1

    y = 160 + distance * 24   # px
    move_to(290, y)  # place cursor on track
    # slight offset to have the subtrack be inserted at the left
    drag_duration = 0.5

    # in grouped track live interface reacts more slower
    if set.current_track_is_grouped:
        drag_duration = 2

    drag_to(x_orig - 40, y_orig, duration=drag_duration)


def save_and_remove_ext_track(set: AbletonSet):
    from loguru import logger
    logger.success(set.current_track_name)
    if set.is_unknown:
        notification_window.delay(
            "Set is unknown", notification_enum=NotificationEnum.WARNING.value
        )
        return

    if set.current_track_type != "ExternalSynthTrack":
        notification_window.delay("Invalid track", notification_enum=NotificationEnum.WARNING.value)
        return

    if not is_browser_splurges_clickable():
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
    y = 180 if set.has_backup else 156
    drag_to(278, y)
    sleep(0.5)
    # save
    send_keys("{ENTER}")
    send_left()
    send_keys("{ENTER}")

    p0_script_client_from_http().dispatch(DeleteSelectedTrackCommand(set.current_track_name))

    move_to(*initial_mouse_position)
    notification_window.delay("Saved", notification_enum=NotificationEnum.SUCCESS.value)

    # checking the track was saved
    sleep(1)
    saved_track = set.last_saved_track
    saved_track_name = basename(saved_track).replace(".als", "")

    if saved_track_name != set.current_track_name or time.time() - os.path.getatime(saved_track) > 2:
        notification_window.delay(
            "Track was not saved",
            notification_enum=NotificationEnum.ERROR.value,
            centered=True,
        )
        return
