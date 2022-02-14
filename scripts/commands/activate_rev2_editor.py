from enum import Enum
from typing import Tuple

from loguru import logger

from config import SystemConfig
from lib.ableton import show_plugins
from lib.click import click
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import get_window_position, focus_window


class Rev2ButtonsRelativeCoordinates(Enum):
    """ These coordinates are relative to the plugin window == Mouse position relative from active_window.ahk """
    ACTIVATION_MIDDLE_BUTTON = (784, 504)
    PROGRAM = (1067, 147)
    PRESET_STAR_CATEGORY = (861, 335)


def _get_absolute_button_position(handle: int, window_coordinates: Rev2ButtonsRelativeCoordinates) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_button, y_button) = window_coordinates.value
    return (x + x_button, y + y_button)


def activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = find_window_handle_by_enum(SystemConfig.REV2_EDITOR_WINDOW_TITLE)
    if not handle:
        logger.warning("Couldn't find rev2 editor window")
        return
    focus_window(name=SystemConfig.REV2_EDITOR_WINDOW_TITLE)
    click(*_get_absolute_button_position(handle, Rev2ButtonsRelativeCoordinates.ACTIVATION_MIDDLE_BUTTON))


def post_activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = find_window_handle_by_enum(SystemConfig.REV2_EDITOR_WINDOW_TITLE)
    if not handle:
        logger.warning("Couldn't find rev2 editor window")
        return
    focus_window(name=SystemConfig.REV2_EDITOR_WINDOW_TITLE)
    click(*_get_absolute_button_position(handle, Rev2ButtonsRelativeCoordinates.PROGRAM))
    click(*_get_absolute_button_position(handle, Rev2ButtonsRelativeCoordinates.PRESET_STAR_CATEGORY))
