import PySimpleGUI as sg
import pyautogui
from PySimpleGUI import POPUP_BUTTONS_NO_BUTTONS
from loguru import logger

from api.p0_script_api_client import protocol0
from lib.decorators import throttle
from lib.errors.Protocol0Error import Protocol0Error

CHAR_DURATION = 0.05


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


@throttle(milliseconds=50)
def show_prompt(question: str) -> None:
    logger.info(GuiState.HAS_DIALOG)
    if GuiState.HAS_DIALOG:
        raise Protocol0Error("a dialog is already shown")

    GuiState.HAS_DIALOG = True
    ok = False
    layout = [
        [sg.Text(question, key="question")],
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
