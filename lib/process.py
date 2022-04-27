import subprocess
import sys

import win32process
from loguru import logger
from psutil import Process, NoSuchProcess

from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


def execute_process_in_new_window(*args: str):
    powershell_command_line = f"'cmd /c start powershell -Command {{ {' '.join(args)} }}'"
    logger.info(powershell_command_line)
    subprocess.run(["powershell.exe",
                    "invoke-expression",
                    powershell_command_line
                    ],
                   stdout=sys.stdout)


def execute_python_script_in_new_window(*args: str):
    execute_process_in_new_window("py -3.7", *args)


def _get_window_pid_by_criteria(name: str, search_type: SearchTypeEnum = SearchTypeEnum.WINDOW_TITLE) -> int:
    handle = find_window_handle_by_enum(name=name, search_type=search_type)
    if handle == 0:
        return 0

    _, pid = win32process.GetWindowThreadProcessId(handle)
    logger.info(f"{name}: found pid {pid}")
    return pid


def kill_window_by_criteria(name: str, search_type: SearchTypeEnum = SearchTypeEnum.WINDOW_TITLE):
    while True:
        pid = _get_window_pid_by_criteria(name=name, search_type=search_type)
        if pid > 0:
            logger.info(f"killing window with pid {pid}")
            try:
                Process(pid=pid).terminate()
            except NoSuchProcess:
                return
        else:
            return
