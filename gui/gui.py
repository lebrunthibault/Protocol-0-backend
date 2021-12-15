from functools import partial
from threading import Timer
from typing import Optional

import PySimpleGUI as sg
import pyautogui

from api.p0_script_api_client import protocol0
from lib.decorators import throttle
from lib.enum.ColorEnum import ColorEnum
from lib.errors.Protocol0Error import Protocol0Error

CHAR_DURATION = 0.05


class GuiState():
    HAS_DIALOG = False
    CURRENT_WINDOW = None
    CURRENT_TIMER: Optional[Timer] = None


def close_current_window():
    if GuiState.CURRENT_WINDOW:
        GuiState.CURRENT_WINDOW.close()
        GuiState.CURRENT_WINDOW = None


def show_message(message: str, auto_close_duration=None, background_color: Optional[ColorEnum] = None):
    close_current_window()
    if auto_close_duration is None:
        auto_close_duration = 2 + len(message) * CHAR_DURATION
    background_color = background_color.hex_value if background_color else None
    window = sg.Window("Message window",
                       layout=[[sg.Text(message, background_color=background_color)]],
                       no_titlebar=True,
                       location=(pyautogui.size()[0] - (80 + 7 * len(message)), 10),
                       background_color=background_color,
                       keep_on_top=True,
                       modal=False,
                       )

    window.read(timeout=0)
    GuiState.CURRENT_WINDOW = window

    from api.midi_app import call_system_method

    t = Timer(auto_close_duration, partial(call_system_method, close_current_window))
    if GuiState.CURRENT_TIMER:
        GuiState.CURRENT_TIMER.cancel()
    GuiState.CURRENT_TIMER = t
    t.start()


@throttle(milliseconds=50)
def show_prompt(question: str, background_color: ColorEnum = None) -> None:
    background_color = background_color.hex_value if background_color else None
    if GuiState.HAS_DIALOG:
        raise Protocol0Error("a dialog is already shown")

    GuiState.HAS_DIALOG = True
    ok = False
    layout = [
        [sg.Text(question, key="question", background_color=background_color)],
        [sg.Input(key="input", visible=False)],
        [sg.Button("ok", key="ok")],
    ]
    window = sg.Window(
        "Dialog Window",
        layout,
        modal=True,
        return_keyboard_events=True,
        keep_on_top=True,
        no_titlebar=True,
        background_color=background_color,
        element_justification='c'
    )
    while True:
        event, values = window.read()
        print(event, type(event), values)
        if event == "Exit" or event == sg.WIN_CLOSED or event.split(":")[0] == "Escape":
            break

        if event == "ok" or (len(event) == 1 and ord(event) == 13):
            ok = True
            break

    window.close()
    GuiState.HAS_DIALOG = False

    protocol0.system_response(ok)
