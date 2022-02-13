from ctypes import windll
from typing import Tuple, Union

import win32com.client
import win32gui
from loguru import logger

from lib.window.find_window import SearchTypeEnum, find_window_handle_by_enum


def get_window_position(handle: int) -> Tuple[int, int, int, int]:
    rect = win32gui.GetWindowRect(handle)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    logger.info("Location: (%d, %d)" % (x, y))
    logger.info("Size: (%d, %d)" % (w, h))
    return int(x), int(y), int(w), int(h)


def focus_window(name: str, search_type: Union[SearchTypeEnum, str] = SearchTypeEnum.WINDOW_TITLE,
                 retry: bool = True) -> None:
    handle = find_window_handle_by_enum(name=name, search_type=search_type)
    logger.info(f"handle: {handle}")
    if not handle:
        logger.info(f"handle not found for {name}")

    try:
        win32gui.SetForegroundWindow(handle)
        return
    except Exception as e:
        logger.error(e)
        if retry:
            # needed for SetForegroundWindow to be allowed
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            focus_window(name=name, search_type=search_type, retry=False)
            return

    logger.error("Window not focused : %s" % name)


def is_window_focused(handle: int) -> bool:
    active_window_handle = windll.user32.GetForegroundWindow()
    if active_window_handle == 0:
        return False
    return handle == active_window_handle
