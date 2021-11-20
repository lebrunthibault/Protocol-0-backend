import time

from lib.decorators import throttle

CHAR_DURATION = 0.05
import PySimpleGUI as sg
import pyautogui
from PySimpleGUI import POPUP_BUTTONS_NO_BUTTONS

from loguru import logger


class GuiState():
    HAS_DIALOG = False


def show_message(message: str, auto_close_duration=None, background_color=None):
    if auto_close_duration is None:
        auto_close_duration = 2 + len(message) * CHAR_DURATION

    sg.popup(message,
             auto_close=True,
             auto_close_duration=auto_close_duration,
             no_titlebar=True,
             location=(pyautogui.size()[0] - (80 + 6 * len(message)), 10),
             background_color=background_color,
             keep_on_top=True,
             # non_blocking=True,
             modal=False,
             button_type=POPUP_BUTTONS_NO_BUTTONS,
             )


@throttle(milliseconds=100)
def show_dialog(message: str, button_label: str, on_success: callable, background_color=None):
    print(GuiState.HAS_DIALOG)
    print(time.time())
    if GuiState.HAS_DIALOG:
        logger.error("a dialog is already shown")
        return

    GuiState.HAS_DIALOG = True
    layout = [
        [sg.Text(message, key="text")],
        [sg.Input(key="input", visible=False)],
        [sg.Button(button_label, key="button")],
    ]
    window = sg.Window(
        "Dialog Window",
        layout,
        modal=True,
        return_keyboard_events=True,
        keep_on_top=True,
        no_titlebar=True,
        element_justification='c'
    )
    while True:
        event, values = window.read()
        print(event, type(event), values)
        if event == "Exit" or event == sg.WIN_CLOSED or event.split(":")[0] == "Escape":
            break

        if event == "button" or (len(event) == 1 and ord(event) == 13):
            on_success()
            break

    window.close()
    GuiState.HAS_DIALOG = False
