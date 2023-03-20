import os
import time
from os.path import isabs

import keyboard
import win32gui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from gui.celery import notification_window
from lib.ableton.get_set import get_ableton_windows
from lib.desktop.desktop import go_to_desktop
from lib.enum.notification_enum import NotificationEnum
from lib.keys import send_keys
from lib.keys import send_right
from lib.mouse.mouse import click, keep_mouse_position
from lib.process import execute_powershell_command
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import (
    is_window_focused,
    focus_window,
    get_focused_window_process_name,
)
from protocol0.application.command.ResetPlaybackCommand import ResetPlaybackCommand

settings = Settings()


def focus_ableton() -> None:
    focus_window(
        settings.ableton_process_name, search_type=SearchTypeEnum.PROGRAM_NAME
    )  # type: ignore


def is_ableton_focused() -> bool:
    return get_focused_window_process_name() == settings.ableton_process_name


def are_logs_focused() -> bool:
    logs_handle = find_window_handle_by_enum(settings.log_window_title, SearchTypeEnum.WINDOW_TITLE)
    return is_window_focused(logs_handle)


def plugins_shown() -> bool:
    return (
        find_window_handle_by_enum(
            "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
        )
        is not None
    )


def show_plugins() -> None:
    if not plugins_shown():
        keyboard.press_and_release("ctrl+alt+p")


def hide_plugins():
    if plugins_shown():
        send_keys("^%p")


def reload_ableton() -> None:
    """
    Not easy to have this work every time
    """
    p0_script_client().dispatch(ResetPlaybackCommand())
    # hack to get the focus when ableton is shown
    go_to_desktop(1)
    go_to_desktop(0)

    for i in range(0, 5):
        if win32gui.GetCursorInfo()[1] == 65543:  # loading
            break

        focus_ableton()
        send_keys("^n")
        send_keys("{RIGHT}")
        time.sleep(0.1)  # when clicking too fast, ableton is opening a template set ..
        if len(get_ableton_windows()) == 2:
            send_keys("{ENTER}")
            break


def save_set():
    send_keys("^s")


@keep_mouse_position
def save_set_as_template(open_pref=True):
    p0_script_client().dispatch(ResetPlaybackCommand())
    if open_pref:
        send_keys("^,")
    else:
        time.sleep(0.01)

    # first possible position
    click((703, 363))  # click on File Folder
    click((1032, 201))  # click on set as new
    time.sleep(0.05)

    # second position possible
    click((703, 332))  # click on File Folder
    click((1032, 203))  # click on set as new (2nd position)
    click((1032, 230))  # click on set as new (2nd position)
    time.sleep(0.05)
    send_keys("{ENTER}")
    time.sleep(0.2)
    send_keys("	{ESC}")
    time.sleep(0.5)

    reload_ableton()


def toggle_fold_set():
    send_keys("{TAB}")
    send_keys("%u")
    time.sleep(0.01)
    send_keys("%u")
    send_keys("{TAB}")


def clear_arrangement():
    time.sleep(0.1)
    click((968, 348))  # click on File Folder
    time.sleep(0.05)
    send_keys("^a")
    time.sleep(0.05)
    send_keys("{BACKSPACE}")


def open_set(set_path: str):
    if not isabs(set_path):
        set_path = f"{settings.ableton_set_directory}\\{set_path}"

    if not os.path.exists(set_path):
        notification_window.delay(f"fichier introuvable : {set_path}", NotificationEnum.ERROR.value)
        return

    relative_path = set_path.replace(f"{settings.ableton_set_directory}\\", "").replace("//", "\\")
    notification_window.delay(f"Opening '{relative_path}'")

    go_to_desktop(0)
    execute_powershell_command(f'& "{settings.ableton_exe}" "{set_path}"')
    from lib.ableton_set import AbletonSetManager

    AbletonSetManager.LAST_SET_OPENED_AT = time.time()
    time.sleep(2)

    for _ in range(6):
        send_right()
        send_keys("{ENTER}")
        time.sleep(0.5)
