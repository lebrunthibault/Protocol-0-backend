import subprocess

from config import Config
from lib.process import kill_window_by_criteria
from lib.window.find_window import SearchTypeEnum


def clear_terminal():
    subprocess.Popen("cls", shell=True).communicate()


def kill_backend_terminal_windows():
    kill_window_by_criteria(name=Config.MIDI_SERVER_WINDOW_TITLE, search_type=SearchTypeEnum.WINDOW_TITLE)
    kill_window_by_criteria(name=Config.SR_WINDOW_TITLE, search_type=SearchTypeEnum.WINDOW_TITLE)
