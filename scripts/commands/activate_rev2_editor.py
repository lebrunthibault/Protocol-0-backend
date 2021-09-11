from typing import Tuple

from lib.click import click
from lib.window.ableton import show_plugins
from lib.window.window import get_window_position, focus_window


def get_button_middle_position(handle):
    # type: (int) -> Tuple[int, int]
    (x, y, w, h) = get_window_position(handle)
    x_button = x + w / 2
    y_button = (float(h) / 1.88) + y
    return (int(x_button), int(y_button))


def activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = focus_window(name="REV2Editor/midi")
    if not handle:
        return
    (x, y) = get_button_middle_position(handle)
    click(x, y)
