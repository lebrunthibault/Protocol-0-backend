from ctypes import windll
from typing import Tuple, Union

import win32com.client
import win32gui
from loguru import logger

from config import SystemConfig
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
                 retry: bool = True) -> int:
    handle = find_window_handle_by_enum(name=name, search_type=search_type)
    if not handle:
        return 0

    try:
        win32gui.SetForegroundWindow(handle)
        return handle
    except Exception as e:
        logger.error(e)
        if retry:
            # needed for SetForegroundWindow to be allowed
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            return focus_window(name=name, search_type=search_type, retry=False)

    logger.error("Window not focused : %s" % name)
    return 0


def focus_ableton() -> bool:
    return focus_window(SystemConfig.ABLETON_EXE, search_type=SearchTypeEnum.PROGRAM_NAME)  # type: ignore


def is_ableton_up() -> bool:
    return find_window_handle_by_enum(SystemConfig.ABLETON_EXE, SearchTypeEnum.PROGRAM_NAME) != 0


def is_ableton_focused() -> bool:
    ableton_handle = find_window_handle_by_enum(SystemConfig.ABLETON_EXE, SearchTypeEnum.PROGRAM_NAME)
    active_window_handle = windll.user32.GetForegroundWindow()
    print(ableton_handle)
    print(active_window_handle)
    return ableton_handle != 0 and ableton_handle == active_window_handle
