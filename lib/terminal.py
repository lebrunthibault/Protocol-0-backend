import subprocess

from config import SystemConfig
from lib.process import kill_window_by_criteria
from lib.window.find_window import SearchTypeEnum


def clear_terminal():
    subprocess.Popen("cls", shell=True).communicate()


def kill_system_terminal_windows():
    kill_window_by_criteria(name=SystemConfig.MIDI_SERVER_WINDOW_TITLE, search_type=SearchTypeEnum.WINDOW_TITLE)
    kill_window_by_criteria(name=SystemConfig.SR_WINDOW_TITLE, search_type=SearchTypeEnum.WINDOW_TITLE)
