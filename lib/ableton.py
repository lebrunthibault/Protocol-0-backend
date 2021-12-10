import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import keyboard

from api.p0_script_api_client import protocol0
from config import SystemConfig
from gui.gui import show_prompt
from lib.ableton_parsing import Clip
from lib.click import click
from lib.keys import send_keys
from lib.process import kill_window_by_criteria
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import is_window_focused, focus_window


@dataclass(frozen=True)
class AbletonInfos():
    ableton_version: str

    @property
    def ableton_major_version(self) -> str:
        return self.ableton_version.split('.')[0]

    @property
    def program_name(self) -> str:
        return f"Ableton Live {self.ableton_major_version} Suite"

    @property
    def preferences_location(self) -> Path:
        return Path(f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {self.ableton_version}\Preferences")

    @property
    def exe_location(self) -> Path:
        return Path(
            f"C:\\ProgramData\\Ableton\\Live {self.ableton_major_version}\\Program\\Ableton Live {self.ableton_major_version} Suite.exe")


def focus_ableton() -> bool:
    return focus_window(SystemConfig.ABLETON_EXE, search_type=SearchTypeEnum.PROGRAM_NAME)  # type: ignore


def is_ableton_up() -> bool:
    return find_window_handle_by_enum(SystemConfig.ABLETON_EXE, SearchTypeEnum.PROGRAM_NAME) != 0


def is_ableton_focused() -> bool:
    ableton_handle = find_window_handle_by_enum(SystemConfig.ABLETON_EXE, SearchTypeEnum.PROGRAM_NAME)
    return is_window_focused(ableton_handle)


def are_logs_focused() -> bool:
    logs_handle = find_window_handle_by_enum(SystemConfig.LOG_WINDOW_TITLE, SearchTypeEnum.WINDOW_TITLE)
    return is_window_focused(logs_handle)


def show_plugins() -> None:
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
        keyboard.press_and_release('ctrl+alt+p')


def analyze_test_audio_clip_jitter(clip_path: str):
    clip_path = f"{clip_path}.asd"
    clip = Clip(clip_path, 44100, 44100)

    warp_markers = clip.warp_markers[1:-1]
    if len(warp_markers) == 8:
        step = 1
    elif len(warp_markers) == 16:  # warp markers on note end
        step = 2
    else:
        protocol0.show_message(f"couldn't analyze jitter, got {len(warp_markers)} warp_markers")
        return

    i = 0
    total_jitter = 0
    # we ignore warp markers set on note end
    for warp_marker in warp_markers[::step]:
        total_jitter += abs(warp_marker.seconds - i * 0.25)
        i += 1

    average_jitter = (total_jitter / 8) * 1000
    message = f"average jitter {average_jitter:.2f} ms"
    protocol0.show_message(message)
    show_prompt(message)


def reload_ableton() -> None:
    if not is_ableton_focused():
        focus_ableton()
        time.sleep(0.5)
    send_keys("^n")
    send_keys("{Right}")
    send_keys("{Right}")
    send_keys("{Right}")
    send_keys("{Right}")
    time.sleep(0.05)  # when clicking too fast, ableton is opening a template set ..
    send_keys("{Enter}")
    send_keys("{Enter}")


def save_set():
    send_keys("^s")


def save_set_as_template(open_pref=False):
    protocol0.reset_song()
    if open_pref:
        send_keys("^,")
    else:
        time.sleep(0.01)
    # first possible position
    click(x=703, y=363)  # click on File Folder
    click(x=1032, y=201)  # click on set as new
    time.sleep(0.05)

    # second position possible
    click(x=703, y=332)  # click on File Folder
    click(x=1032, y=203)  # click on set as new (2nd position)
    click(x=1032, y=230)  # click on set as new (2nd position)
    time.sleep(0.05)
    send_keys("{Enter}")
    time.sleep(0.2)
    send_keys("	{ESC}")


def clear_arrangement():
    click(x=968, y=348)  # click on File Folder
    time.sleep(0.05)
    send_keys("^a")
    time.sleep(0.05)
    send_keys("{BACKSPACE}")


def kill_ableton():
    kill_window_by_criteria(name=SystemConfig.ABLETON_WINDOW_CLASS_NAME, search_type=SearchTypeEnum.WINDOW_CLASS_NAME)

    # # remove crash files
    # crash_folder = ableton_locations.preferences_location / "Crash"
    # if crash_folder.exists():
    #     shutil.rmtree(crash_folder)
    # unlink_if_exists(ableton_locations.preferences_location / "CrashDetection.cfg")
    # unlink_if_exists(ableton_locations.preferences_location / "CrashRecoveryInfo.cfg")
    # unlink_if_exists(ableton_locations.preferences_location / "Log.txt")


def restart_ableton():
    kill_ableton()

    # restart
    ableton_locations = AbletonInfos(ableton_version=SystemConfig.ABLETON_VERSION)
    subprocess.run([ableton_locations.exe_location])
