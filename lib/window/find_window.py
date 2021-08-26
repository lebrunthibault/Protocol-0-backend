import enum
import logging
from functools import partial
from typing import Optional, Any, List, Dict, Union

import win32api
import win32con
import win32gui
import win32process
import wmi

from lib.errors.Protocol0Error import Protocol0Error

logger = logging.getLogger(__name__)

c = wmi.WMI()


class SearchTypeEnum(enum.Enum):
    NAME = "NAME"
    EXE = "EXE"
    CLASS = "CLASS"


def find_window_handle_by_enum(name: str, search_type: Union[SearchTypeEnum, str]) -> int:
    if search_type == SearchTypeEnum.NAME:
        find_func = partial(find_window_handle_by_criteria, title=name)
    elif search_type == SearchTypeEnum.EXE:
        find_func = partial(find_window_handle_by_criteria, app_name=name)
    elif search_type == SearchTypeEnum.CLASS:
        find_func = partial(find_window_handle_by_criteria, class_name=name)
    else:
        raise Protocol0Error("Invalid enum value %s" % search_type)

    return find_func()


def find_window_handle_by_criteria(class_name: Optional[str] = None, app_name: Optional[str] = None,
                                   title: Optional[str] = None) -> int:
    assert class_name or app_name or title, "You should give a criteria to search a window"

    handle = 0

    def winEnumHandler(hwnd, _):
        # type: (int, Any) -> None
        nonlocal handle
        handle_app_name = _get_app_name(hwnd)
        if handle_app_name == "chrome.exe":
            return
        if (
            win32gui.IsWindowVisible(hwnd)
            and (not class_name or win32gui.GetClassName(hwnd) == class_name)
            and (not app_name or handle_app_name == app_name)
        ):
            handle = hwnd

    if title:
        handle = win32gui.FindWindow(None, title)
    else:
        win32gui.EnumWindows(winEnumHandler, None)

    if handle:
        logger.info(f"Window handle found : {handle}, app_name: {_get_app_name(handle)}")
    else:
        logger.info(
            f"Window handle not found. class_name={class_name}, app_name={app_name}, title={title}")

    return handle


def show_windows(_app_name_black_list: List[str] = None) -> List[Dict]:
    app_name_black_list = _app_name_black_list if _app_name_black_list else [
        "explorer.exe", "chrome.exe", "ipoint.exe", "TextInputHost.exe"
    ]
    class_name_black_list = [
        "ThumbnailDeviceHelperWnd", "Shell_TrayWnd", "wxWindowNR"
    ]

    result = []

    def winEnumHandler(hwnd, _):
        # type: (int, Any) -> None
        nonlocal result
        if win32gui.IsWindowVisible(hwnd):
            name = _get_window_title(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            app_name = _get_app_name(hwnd)
            if not app_name:
                return
            if "too" in app_name_black_list or class_name in class_name_black_list:
                return
            line = {
                "name": name,
                "class_name": class_name,
                "app_name": app_name
            }
            logger.info(line)
            result.append(line)

    win32gui.EnumWindows(winEnumHandler, None)

    return result


def _get_window_title(hwnd: int) -> str:
    return win32gui.GetWindowText(hwnd)


def _get_app_name(hwnd: int) -> Optional[str]:
    """Get application base name given hwnd."""
    pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
        return win32process.GetModuleFileNameEx(handle, 0).split("\\")[-1]
    except Exception as e:
        logger.error(e)
        return None


def get_pid_by_window_name(name: str) -> int:
    hwnd = find_window_handle_by_criteria(title=name)
    if hwnd == 0:
        return 0

    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid
