import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import keyboard
from loguru import logger
from protocol0.application.command.ResetSongCommand import ResetSongCommand

from api.p0_script_api_client import p0_script_client
from config import SystemConfig
from lib.ableton_parsing import Clip
from lib.click import click
from lib.enum.ColorEnum import ColorEnum
from lib.keys import send_keys
from lib.process import kill_window_by_criteria
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import is_window_focused, focus_window
from message_queue.celery import notification


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


def focus_ableton() -> None:
    focus_window(SystemConfig.ABLETON_EXE, search_type=SearchTypeEnum.PROGRAM_NAME)  # type: ignore


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
    # NB at 44100 the sample rate induced max jitter is 0.023 ms
    notes_count = 8 - 1

    # skipping start and end markers, excepting notes_count markers
    warp_markers = [wm for wm in clip.warp_markers if wm.seconds >= 0.125 and wm.seconds <= 1.875][0:notes_count]

    if len(warp_markers) != notes_count:
        message = f"couldn't analyze jitter, got {len(warp_markers)} central warp_markers, expected {notes_count}"
        notification.delay(message)
        return

    beat_offsets = []
    # we ignore warp markers set on note end
    for i, warp_marker in enumerate(warp_markers):  # 1 in case the recording started before 1.1.1
        beat_offsets.append((warp_marker.seconds - (i + 1) * 0.25) * 1000)

    average_latency = (sum(beat_offsets) / notes_count)
    total_jitter = sum(abs(b - average_latency) for b in beat_offsets)
    average_jitter = (total_jitter / notes_count)
    message = f"average jitter {average_jitter:.2f} ms\naverage latency {average_latency:.2f} ms"
    logger.info(message)
    background_color = ColorEnum.SUCCESS
    if average_jitter > 1 or average_latency < 0:
        background_color = ColorEnum.WARNING

    notification.delay(message)


def reload_ableton() -> None:
    if not is_ableton_focused():
        focus_ableton()
        time.sleep(0.2)
    send_keys("^n")
    send_keys("{Right}")
    # NB : we have a problem of double set load when doing it programmatically
    # send_keys("{Right}")
    # send_keys("{Right}")
    # send_keys("{Right}")
    time.sleep(0.1)  # when clicking too fast, ableton is opening a template set ..
    # don't save set
    send_keys("{Enter}")
    # # but keep recordings
    # send_keys("{Right}")
    # send_keys("{Enter}")


def save_set():
    send_keys("^s")


def save_set_as_template(open_pref=False):
    p0_script_client.dispatch(ResetSongCommand())
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

    reload_ableton()


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
