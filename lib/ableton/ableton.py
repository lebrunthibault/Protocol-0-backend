import os
import time
from os.path import isabs

import keyboard
import pyautogui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from gui.celery import notification_window
from lib.desktop.desktop import go_to_desktop
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys, send_right
from lib.mouse.mouse import click
from lib.process import execute_process_in_new_window
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


def show_plugins() -> None:
    if not find_window_handle_by_enum(
        "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
    ):
        keyboard.press_and_release("ctrl+alt+p")


def reload_ableton() -> None:
    """
    Not easy to have this work every time
    """
    p0_script_client().dispatch(ResetPlaybackCommand())
    go_to_desktop(0)

    time.sleep(0.5)
    focus_ableton()
    # time.sleep(0.5)

    send_keys("^n")
    send_keys("{RIGHT}")
    time.sleep(0.1)  # when clicking too fast, ableton is opening a template set ..
    send_keys("{ENTER}")


def save_set():
    send_keys("^s")


def save_set_as_template(open_pref=True):
    p0_script_client().dispatch(ResetPlaybackCommand())
    if open_pref:
        send_keys("^,")
    else:
        time.sleep(0.01)

    initial_mouse_position = pyautogui.position()

    # first possible position
    click(x=703, y=363, keep_position=False)  # click on File Folder
    click(x=1032, y=201, keep_position=False)  # click on set as new
    time.sleep(0.05)

    # second position possible
    click(x=703, y=332, keep_position=False)  # click on File Folder
    click(x=1032, y=203, keep_position=False)  # click on set as new (2nd position)
    click(x=1032, y=230, keep_position=False)  # click on set as new (2nd position)
    time.sleep(0.05)
    send_keys("{ENTER}")
    time.sleep(0.2)
    send_keys("	{ESC}")

    reload_ableton()

    # restore mouse position
    pyautogui.moveTo(initial_mouse_position)


def toggle_fold_set():
    send_keys("{TAB}")
    send_keys("%u")
    time.sleep(0.01)
    send_keys("%u")
    send_keys("{TAB}")


def clear_arrangement():
    time.sleep(0.1)
    click(x=968, y=348)  # click on File Folder
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
    execute_process_in_new_window(f'& "{set_path}"')
    time.sleep(2)

    for _ in range(6):
        send_right()
        send_keys("{ENTER}")
        time.sleep(0.5)


def toggle_clip_notes():
    click(87, 1015, keep_position=True)
