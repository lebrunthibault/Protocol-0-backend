from ctypes import windll
from time import sleep
from typing import Tuple, Union

# noinspection PyUnresolvedReferences
import psutil
import pythoncom
import win32com.client
import win32gui
import win32process
from loguru import logger
from psutil import NoSuchProcess

from lib.errors.Protocol0Error import Protocol0Error
from lib.window.find_window import SearchTypeEnum, find_window_handle_by_enum


def get_window_position(handle: int) -> Tuple[int, int, int, int]:
    rect = win32gui.GetWindowRect(handle)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    return int(x), int(y), int(w), int(h)


def focus_window(
    name: str,
    search_type: Union[SearchTypeEnum, str] = SearchTypeEnum.WINDOW_TITLE,
    retry: bool = True,
) -> int:
    handle = find_window_handle_by_enum(name=name, search_type=search_type)
    assert handle, f"No window '{name}'"

    # noinspection PyUnresolvedReferences
    pythoncom.CoInitialize()  # needed
    # noinspection PyBroadException
    try:
        win32gui.SetForegroundWindow(handle)
        return handle
    except Exception as e:
        logger.warning(f"couldn't focus {name} : {e}")
        if retry:
            # needed for SetForegroundWindow to be allowed
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("%")
            return focus_window(name=name, search_type=search_type, retry=False)

    logger.error("Window not focused : %s" % name)
    raise Protocol0Error("window is not focused")


def move_window(handle, x: int, y: int, w: int, h: int):
    # see https://stackoverflow.com/questions/51694887/win32gui-movewindow-not-aligned-with-left-edge-of-screen
    win32gui.MoveWindow(handle, x - 7, y, w, h, True)
    sleep(0.1)


def is_window_focused(handle: int) -> bool:
    active_window_handle = windll.user32.GetForegroundWindow()
    return active_window_handle != 0 and handle == active_window_handle


def get_focused_window_process_name():
    res = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    pid = res[-1]
    if pid < 0:
        logger.warning(f"Got pid {pid}")
        return ""

    try:
        return psutil.Process(pid).name()
    except NoSuchProcess:
        return ""


def get_focused_window_title() -> str:
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())
