import ctypes
import os
import re
import sys
import time
from dataclasses import dataclass

import win32con
import win32gui
from loguru import logger
from psutil import Process, NoSuchProcess
from rx import operators as op, create
from rx.disposable import Disposable

from config import LOGGING_DIRECTORY
from lib.console import clear_console
from lib.window.find_window import get_pid_by_window_name
from lib.window.window import focus_window
from sr.rx.rx_utils import rx_error

logger = logger.opt(colors=True)

VERSION = os.environ["abletonVersion"]


class Config:
    PROCESS_LOGS = True
    WINDOW_TITLE = "logs terminal"
    LOG_FILENAME = f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {VERSION}\\Preferences\\Log.txt"
    START_SIZE = 70
    COLOR_SCHEME = {
        "P0 - dev": "yellow",
        "P0 - debug": "black",
        "P0 - info": "green",
        "P0 - notice": "blue",
        "P0 - warning": "magenta",
        "P0 - error": "red",
        "P0": "green",
        "Protocol0": "green",
        "error": "red",
        "exception": "red",
    }
    FILTER_KEYWORDS = ["P0", "Protocol0", "ArgumentError", "RemoteScriptError", "Exception"]
    FOCUS_WINDOW_KEYWORDS = ["error", "exception"]
    CLEAR_KEYWORDS = ["clear_logs", "(Protocol0) Initializing", "Check :"]
    PATTERNS_TO_REMOVE = [
        "P0 - (\w+:)?",
        "Python: INFO:root:\d* - ",
        "(info|debug):\s?",
        "RemoteScriptError: ",
        "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\:",
    ]


logger.remove()
logger.add(sys.stdout, format="<light-yellow>{time:HH:mm:ss.SS}</> {message}")
logger.add(f"{LOGGING_DIRECTORY}\\logs.log", level="ERROR")


@dataclass()
class LogLine():
    line: str
    color: str = "white"

    def __str__(self):
        return f"<{self.color}>{self.line.strip()}</>"


def _kill_previous_log_window():
    while True:
        pid = get_pid_by_window_name(Config.WINDOW_TITLE)
        if pid > 0:
            try:
                Process(pid=pid).terminate()
            except NoSuchProcess:
                return
        else:
            return


def _remove_pattern_from_line(line: LogLine):
    for pattern in Config.PATTERNS_TO_REMOVE:
        line.line = re.sub(pattern, "", line.line)

    return line


def _focus_logs_on_pattern(line: str) -> None:
    if any(keyword.lower() in line.lower() for keyword in Config.FOCUS_WINDOW_KEYWORDS):
        focus_window(Config.WINDOW_TITLE)


def _filter_line(line: str) -> bool:
    if any(keyword.lower() in line.lower() for keyword in Config.CLEAR_KEYWORDS):
        clear_console()
        return False

    return any(keyword.lower() in line.lower() for keyword in Config.FILTER_KEYWORDS)


def _select_line_color(line: LogLine) -> LogLine:
    for sub_string, color in Config.COLOR_SCHEME.items():
        if sub_string.lower() in line.line.lower():
            line.color = color
            break

    return line


def get_line_observable_from_file(file):
    sleep_sec = 0.1

    def _make_observable(observer, _) -> Disposable:
        """ Yield each line from a file as they are written.
         `sleep_sec` is the time to sleep after empty reads. """
        line = ''
        for line in file.readlines()[-Config.START_SIZE:]:
            observer.on_next(line)
        while True:
            tmp = file.readline()
            if tmp is not None:
                line += tmp
                if line.endswith("\n"):
                    observer.on_next(line)
                    line = ''
            elif sleep_sec:
                time.sleep(sleep_sec)

        return Disposable()

    return create(_make_observable)


def tail_ableton_log_file():
    _kill_previous_log_window()

    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SHOW_FULLSCREEN)
    ctypes.windll.kernel32.SetConsoleTitleW(Config.WINDOW_TITLE)

    clear_console()

    pipes = [
        op.map(lambda line: line.replace("\n", "")),
        op.map(lambda line: line.replace("<", "\<")),
    ]

    if Config.PROCESS_LOGS:
        pipes += [
            op.filter(_filter_line),
            op.do_action(_focus_logs_on_pattern),
            op.map(lambda line: LogLine(line=line)),
            op.map(_select_line_color),
            op.map(_remove_pattern_from_line),
        ]

    with open(Config.LOG_FILENAME, 'r') as file:
        log_obs = get_line_observable_from_file(file)
        log_obs.pipe(*pipes).subscribe(logger.info, rx_error)


if __name__ == '__main__':
    try:
        tail_ableton_log_file()
    except Exception as e:
        logger.exception(e)
