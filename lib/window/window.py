import logging
from typing import Tuple

import win32com.client
import win32gui
from a_protocol_0.consts import ABLETON_EXE

from lib.window.find_window import SearchTypeEnum, find_window_handle_by_enum

# needed for SetForegroundWindow to be allowed
shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')


def get_window_position(handle: int) -> Tuple[int, int, int, int]:
    rect = win32gui.GetWindowRect(handle)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    logging.info("Location: (%d, %d)" % (x, y))
    logging.info("Size: (%d, %d)" % (w, h))
    return (int(x), int(y), int(w), int(h))


def focus_window(name: str, search_type=SearchTypeEnum.NAME, retry=True):
    handle = find_window_handle_by_enum(name=name, search_type=search_type)
    if handle:
        try:
            win32gui.SetForegroundWindow(handle)
        except Exception as e:
            logging.error(e)
            if retry:
                shell.SendKeys('%')
                focus_window(name=name, search_type=search_type, retry=False)
        logging.info("Window focused : %s" % name)


def focus_ableton():
    # type: () -> None
    focus_window(ABLETON_EXE, search_type=SearchTypeEnum.EXE)  # type: ignore
