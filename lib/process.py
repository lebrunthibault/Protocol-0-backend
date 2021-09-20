import os.path
import subprocess
import sys

import win32process
from psutil import Process, NoSuchProcess

from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


def execute_in_new_window(path: str, *args):
    assert path.endswith(".py")
    cwd = os.path.dirname(path)
    basename = os.path.basename(path)
    p = subprocess.Popen(["powershell.exe",
                          "jsinvoke-expression",
                          f"'cmd /c start powershell -Command {{ set-location \"%s\"; py {basename} {' '.join(args)} }}'" % cwd],
                         stdout=sys.stdout)
    p.communicate()


def _get_window_pid_by_criteria(name: str, search_type: SearchTypeEnum = SearchTypeEnum.WINDOW_TITLE) -> int:
    hwnd = find_window_handle_by_enum(name=name, search_type=search_type)
    if hwnd == 0:
        return 0

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def kill_window_by_criteria(name: str, search_type: SearchTypeEnum = SearchTypeEnum.WINDOW_TITLE):
    while True:
        pid = _get_window_pid_by_criteria(name=name, search_type=search_type)
        if pid > 0:
            try:
                Process(pid=pid).terminate()
            except NoSuchProcess:
                return
        else:
            return
