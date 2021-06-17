import logging
from typing import Tuple

import win32gui

from lib.click import click
from lib.window.ableton import show_plugins
from lib.window.window import get_window_position

logger = logging.getLogger(__name__)


def get_button_middle_position(handle):
    # type: (int) -> Tuple[int, int]
    (x, y, w, h) = get_window_position(handle)
    x_button = x + w / 2
    y_button = (float(h) / 1.88) + y
    return (int(x_button), int(y_button))


def activate_rev2_editor():
    # type: () -> None
    show_plugins()
    handle = win32gui.FindWindowEx(None, None, None, "REV2Editor/midi")
    logger.info("found handle for rev2 editor: %s" % handle)
    if not handle:
        return
    (x, y) = get_button_middle_position(handle)
    win32gui.SetForegroundWindow(handle)
    click(x, y)
