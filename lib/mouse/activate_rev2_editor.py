from enum import Enum
from loguru import logger
from typing import Tuple

from config import Config
from lib.ableton.ableton import show_plugins
from lib.mouse.mouse import click
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import get_window_position, focus_window


class Rev2ButtonsRelativeCoordinates(Enum):
    """These coordinates are relative to the plugin message == Mouse position relative from active_window.ahk"""

    # Relative coordinates
    ACTIVATION_MIDDLE_BUTTON = (784, 504)
    PROGRAM = (1067, 147)
    PRESET_STAR_CATEGORY = (919, 322)


def _get_absolute_button_position(
    handle: int, window_coordinates: Rev2ButtonsRelativeCoordinates
) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_button, y_button) = window_coordinates.value
    x_button *= Config.DISPLAY_RESOLUTION_FACTOR
    y_button *= Config.DISPLAY_RESOLUTION_FACTOR
    return (x + x_button, y + y_button)


def activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = find_window_handle_by_enum(Config.REV2_EDITOR_WINDOW_TITLE)
    if not handle:
        logger.warning(f"Couldn't find rev2 editor window for name: {Config.REV2_EDITOR_WINDOW_TITLE}. Check set naming")
        return
    focus_window(name=Config.REV2_EDITOR_WINDOW_TITLE)
    click(
        *_get_absolute_button_position(
            handle, Rev2ButtonsRelativeCoordinates.ACTIVATION_MIDDLE_BUTTON
        ),
        exact=True
    )


def post_activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = find_window_handle_by_enum(Config.REV2_EDITOR_WINDOW_TITLE)
    if not handle:
        logger.warning(f"Couldn't find rev2 editor window for name: {Config.REV2_EDITOR_WINDOW_TITLE}. Check set naming")
        return
    focus_window(name=Config.REV2_EDITOR_WINDOW_TITLE)
    click(
        *_get_absolute_button_position(handle, Rev2ButtonsRelativeCoordinates.PROGRAM), exact=True
    )
    click(
        *_get_absolute_button_position(handle, Rev2ButtonsRelativeCoordinates.PRESET_STAR_CATEGORY),
        exact=True
    )
