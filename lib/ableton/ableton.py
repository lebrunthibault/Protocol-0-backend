import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import keyboard

from api.client.p0_script_api_client import p0_script_client
from config import Config
from gui.celery import notification_window
from lib.desktop.desktop import go_to_desktop
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys
from lib.mouse.mouse import click
from lib.process import kill_window_by_criteria, execute_process_in_new_window
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import is_window_focused, focus_window
from protocol0.application.command.ResetSongCommand import ResetSongCommand


@dataclass(frozen=True)
class AbletonInfos:
    ableton_version: str

    @property
    def ableton_major_version(self) -> str:
        return self.ableton_version.split(".")[0]

    @property
    def program_name(self) -> str:
        return f"Ableton Live {self.ableton_major_version} Suite"

    @property
    def preferences_location(self) -> Path:
        return Path(
            f"C:\\Users\\thiba\\AppData\\Roaming\\Ableton\\Live {self.ableton_version}\Preferences"
        )

    @property
    def exe_location(self) -> Path:
        return Path(
            f"C:\\ProgramData\\Ableton\\Live {self.ableton_major_version}\\Program\\Ableton Live {self.ableton_major_version} Suite.exe"
        )


def focus_ableton() -> None:
    focus_window(
        Config.ABLETON_PROCESS_NAME, search_type=SearchTypeEnum.PROGRAM_NAME
    )  # type: ignore


def is_ableton_up() -> bool:
    return find_window_handle_by_enum(Config.ABLETON_PROCESS_NAME, SearchTypeEnum.PROGRAM_NAME) != 0


def is_ableton_focused() -> bool:
    ableton_handle = find_window_handle_by_enum(
        Config.ABLETON_PROCESS_NAME, SearchTypeEnum.PROGRAM_NAME
    )
    return is_window_focused(ableton_handle)


def are_logs_focused() -> bool:
    logs_handle = find_window_handle_by_enum(Config.LOG_WINDOW_TITLE, SearchTypeEnum.WINDOW_TITLE)
    return is_window_focused(logs_handle)


def show_plugins() -> None:
    if not find_window_handle_by_enum(
        "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
    ):
        keyboard.press_and_release("ctrl+alt+p")


def reload_ableton() -> None:
    """
    Not easy to have this work every time
    """
    p0_script_client().dispatch(ResetSongCommand())
    go_to_desktop(0)

    time.sleep(0.5)
    focus_ableton()
    send_keys("^w")  # close the microsoft office popup ..
    time.sleep(0.5)

    send_keys("^n")
    send_keys("{Right}")
    time.sleep(0.1)  # when clicking too fast, ableton is opening a template set ..
    send_keys("{Enter}")


def save_set():
    send_keys("^s")


def save_set_as_template(open_pref=True):
    p0_script_client().dispatch(ResetSongCommand())
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
    kill_window_by_criteria(
        name=Config.ABLETON_WINDOW_CLASS_NAME, search_type=SearchTypeEnum.WINDOW_CLASS_NAME
    )

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
    ableton_locations = AbletonInfos(ableton_version=Config.ABLETON_VERSION)
    subprocess.run([ableton_locations.exe_location])


def open_set(filename: str):
    if not os.path.exists(filename):
        notification_window.delay(f"fichier introuvable : {filename}", NotificationEnum.ERROR.value)
        return

    go_to_desktop(0)
    execute_process_in_new_window(f'& "{filename}"')
