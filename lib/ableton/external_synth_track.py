from enum import Enum
from typing import Tuple

from gui.celery import notification_window

from api.settings import Settings
from lib.ableton.ableton import show_plugins
from lib.enum.NotificationEnum import NotificationEnum
from lib.mouse.mouse import click
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import get_window_position, focus_window

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
        notification_window.delay(
            f"Couldn't focus rev2 editor",
            notification_enum=NotificationEnum.WARNING.value,
        )
        return
    focus_window(name=settings.rev2_editor_window_title)
    click(
        *_get_absolute_button_position(handle, coordinates),
        exact=True,
    )
