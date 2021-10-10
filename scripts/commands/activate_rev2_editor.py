from enum import Enum
from typing import Tuple

from config import SystemConfig
from lib.click import click
from lib.window.ableton import show_plugins
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import get_window_position, focus_window, is_window_focused


class ButtonsRelativeCoordinates(Enum):
    """ These coordinates are relative to the plugin window == Mouse position relative from active_window.ahk """
    ACTIVATION = (784, 504)
    PROGRAM = (1067, 147)
    PRESET_STAR_CATEGORY = (933, 320)


def _get_absolute_button_position(handle: int, window_coordinates: ButtonsRelativeCoordinates) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_button, y_button) = window_coordinates.value
    return (x + x_button, y + y_button)


def activate_rev2_editor():
    # type: () -> None
    handle = find_window_handle_by_enum(SystemConfig.REV2_EDITOR_WINDOW_CLASS_NAME, SearchTypeEnum.WINDOW_CLASS_NAME)
    if is_window_focused(handle):
        return
    show_plugins()
    handle = focus_window(name="REV2Editor/midi")
    if not handle:
        return
    click(*_get_absolute_button_position(handle, ButtonsRelativeCoordinates.ACTIVATION))


def post_activate_rev2_editor():
    # type: () -> None
    handle = find_window_handle_by_enum(SystemConfig.REV2_EDITOR_WINDOW_CLASS_NAME, SearchTypeEnum.WINDOW_CLASS_NAME)
    if not is_window_focused(handle):
        show_plugins()
        handle = focus_window(name="REV2Editor/midi")
    if not handle:
        return
    click(*_get_absolute_button_position(handle, ButtonsRelativeCoordinates.PROGRAM))
    click(*_get_absolute_button_position(handle, ButtonsRelativeCoordinates.PRESET_STAR_CATEGORY))
