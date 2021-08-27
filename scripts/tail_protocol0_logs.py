import ctypes
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Optional

import win32con
import win32gui
from config import LOGGING_DIRECTORY
from lib.console import clear_console
from lib.window.find_window import get_pid_by_window_name
from lib.window.window import focus_window
from loguru import logger
from psutil import Process, NoSuchProcess
from rx import operators as op, create
from sr.rx.rx_utils import rx_error

logger = logger.opt(colors=True)

VERSION = os.environ["abletonVersion"]


class Config:
    PROCESS_LOGS = True
    WINDOW_TITLE = "logs terminal"
    LOG_FILENAME = f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {VERSION}\\Preferences\\Log.txt"
    START_SIZE = 250
    IN_ERROR = True
    COLOR_SCHEME = {
        "yellow": ["P0 - dev", "P0 - debug"],
        "blue": ["P0 - notice"],
        "magenta": ["P0 - warning"],
        "green": ["P0 - info", "Protocol0", "P0"],
    }
    FILTER_KEYWORDS = ["P0", "Protocol0"]
    ERROR_KEYWORDS = ["traceback", "error", "exception"]
    CLEAR_KEYWORDS = ["clear_logs", "(Protocol0) Initializing", "Check :"]
    PATTERNS_TO_REMOVE = [
        "P0 - (\\w+:)?",
        "Python: INFO:root:\\d* - ",
        "(info|debug):\\s?",
        "RemoteScriptError: ",
        "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{6}\\:",
    ]


logger.remove()
logger.add(sys.stdout, format="<light-yellow>{time:HH:mm:ss.SS}</> {message}")
logger.add(f"{LOGGING_DIRECTORY}\\logs.log", level="DEBUG")


@dataclass(frozen=True)
class LogLine:
    line: str
    color: Optional[str] = None
    is_error: bool = False

    def __str__(self):
        color = "red" if self.is_error else (self.color or "white")
        return f"<{color}>{self.line}</>"


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


def _get_clean_line(log_line: LogLine) -> str:
    line = log_line.line
    for pattern in Config.PATTERNS_TO_REMOVE:
        line = re.sub(pattern, "", line)

    return line


def _filter_line(line: LogLine) -> bool:
    if line.is_error:
        return True

    if any(keyword.lower() in line.line.lower() for keyword in Config.CLEAR_KEYWORDS):
        clear_console()
        return False

    if any(keyword.lower() in line.line.lower() for keyword in Config.FILTER_KEYWORDS):
        return True


def _is_error(line: LogLine) -> bool:
    if any(keyword.lower() in line.line.lower() for keyword in Config.ERROR_KEYWORDS):
        # if any(line.line.lower().startswith(keyword.lower()) for keyword in Config.ERROR_KEYWORDS):
        Config.IN_ERROR = True
        focus_window(Config.WINDOW_TITLE)
        return True

    if not line.line.startswith(" "):
        Config.IN_ERROR = False
    else:
        return Config.IN_ERROR


def _get_color(line: LogLine) -> str:
    for color, sub_strings in Config.COLOR_SCHEME.items():
        if any(sub_string.lower() in line.line.lower() for sub_string in sub_strings):
            return color


def get_line_observable_from_file(file):
    sleep_sec = 0.1

    def _make_observable(observer, _):
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

    # noinspection PyTypeChecker
    return create(_make_observable)


def tail_ableton_log_file():
    _kill_previous_log_window()

    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SHOW_FULLSCREEN)
    ctypes.windll.kernel32.SetConsoleTitleW(Config.WINDOW_TITLE)

    # clear_console()

    pipes = [
        op.map(lambda line: line.replace("\n", "")),
        op.map(lambda line: line.replace("<", "\\<")),
    ]

    if Config.PROCESS_LOGS:
        pipes += [
            op.map(lambda line: LogLine(line=line)),
            op.map(lambda line: LogLine(line=line.line, is_error=_is_error(line))),
            op.filter(_filter_line),
            op.map(lambda line: LogLine(line=line.line, is_error=line.is_error, color=_get_color(line))),
            op.map(lambda line: LogLine(line=_get_clean_line(line), is_error=line.is_error, color=line.color)),
        ]

    with open(Config.LOG_FILENAME, 'r') as file:
        log_obs = get_line_observable_from_file(file)
        log_obs.pipe(*pipes).subscribe(logger.info, rx_error)


if __name__ == '__main__':
    try:
        tail_ableton_log_file()
    except Exception as e:
        logger.exception(e)
