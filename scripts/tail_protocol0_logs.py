import ctypes
import re
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

import click
import win32con
import win32gui
from loguru import logger
from psutil import Process, NoSuchProcess
from rx import operators as op, create

from config import SystemConfig
from lib.console import clear_console
from lib.rx import rx_error
from lib.window.find_window import get_pid_by_window_title
from lib.window.window import focus_window

logger = logger.opt(colors=True)


class LogLevelEnum(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"


class Config:
    PROCESS_LOGS = True
    WINDOW_TITLE = "logs terminal"
    LOG_FILENAME = f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {SystemConfig.ABLETON_VERSION}\\Preferences\\Log.txt"
    START_SIZE = 100
    IN_ERROR = False
    LOG_LEVEL = LogLevelEnum.INFO
    COLOR_SCHEME = {
        "light-yellow": ["P0 - dev", "P0 - debug"],
        "light-blue": ["P0 - notice"],
        "magenta": ["P0 - warning"],
        "green": ["P0 - info", "Protocol0", "P0"],
    }
    BLACK_LIST_KEYWORDS = ["Midi(Out|In)Device", "MidiRemoteScript", "Python: INFO:_Framework.ControlSurface:"]
    FILTER_KEYWORDS = ["P0", "Protocol0"]
    ERROR_NON_KEYWORDS = ['\.wav. could not be opened']
    ERROR_KEYWORDS = ["P0 - error", "traceback", "RemoteScriptError", "ArgumentError", "exception"]
    CLEAR_KEYWORDS = ["clear_logs", "\(Protocol0\) Initializing", "Check :"]
    PATTERNS_TO_REMOVE = [
        "P0 - (\\w+:)?",
        "Python: INFO:root:\\d* - ",
        "(info|debug):\\s?",
        "RemoteScriptError: ",
        "RemoteScriptMessage: ",
        "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{6}\\:",
    ]


logger.remove()
logger.add(sys.stdout, format="<light-yellow>{time:HH:mm:ss.SS}</> {message}")
logger.add(f"{SystemConfig.LOGGING_DIRECTORY}\\logs.log", level="DEBUG")


@dataclass(frozen=True)
class LogLine:
    line: str
    color: Optional[str] = None
    is_error: bool = False

    def __str__(self):
        color = "red" if self.is_error else (self.color or "white")
        return f"<{color}>{self.line}</>"

    def has_patterns(self, patterns: List[str]):
        return any(re.search(pattern.lower(), self.line.lower()) for pattern in patterns)


def _kill_previous_log_window():
    while True:
        pid = get_pid_by_window_title(Config.WINDOW_TITLE)
        if pid > 0:
            try:
                Process(pid=pid).terminate()
            except NoSuchProcess:
                return
        else:
            return


def _get_clean_line(line: str) -> str:
    for pattern in Config.PATTERNS_TO_REMOVE:
        line = re.sub(pattern, "", line)

    return line[2:] if line.startswith("  ") else line


def _filter_line(line: LogLine) -> bool:
    if line.is_error:
        return True

    if line.has_patterns(Config.CLEAR_KEYWORDS):
        clear_console()
        return False

    return not line.has_patterns(Config.BLACK_LIST_KEYWORDS) and line.has_patterns(Config.FILTER_KEYWORDS)


def _is_error(line: LogLine) -> bool:
    if line.has_patterns(Config.ERROR_KEYWORDS) and not line.has_patterns(Config.ERROR_NON_KEYWORDS):
        Config.IN_ERROR = True
        focus_window(Config.WINDOW_TITLE)
        return True

    if not _get_clean_line(line.line).startswith(" "):
        Config.IN_ERROR = False

    return Config.IN_ERROR


def _get_color(line: LogLine) -> str:
    for color, sub_strings in Config.COLOR_SCHEME.items():
        if line.has_patterns(sub_strings):
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


@click.command()
@click.option('--raw', is_flag=True)
def tail_ableton_log_file(raw: bool):
    if raw:
        Config.PROCESS_LOGS = False

    _kill_previous_log_window()

    win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SHOW_FULLSCREEN)
    ctypes.windll.kernel32.SetConsoleTitleW(Config.WINDOW_TITLE)

    # clear_console()

    if Config.LOG_LEVEL == LogLevelEnum.INFO:
        Config.BLACK_LIST_KEYWORDS.append("P0 - debug")

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
            op.map(lambda line: LogLine(line=_get_clean_line(line.line), is_error=line.is_error, color=line.color)),
        ]

    with open(Config.LOG_FILENAME, 'r') as file:
        log_obs = get_line_observable_from_file(file)
        log_obs.pipe(*pipes).subscribe(logger.info, rx_error)


if __name__ == '__main__':
    try:
        tail_ableton_log_file()
    except Exception as e:
        logger.exception(e)
