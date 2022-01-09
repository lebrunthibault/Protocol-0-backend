from functools import partial
from threading import Timer
from typing import Optional, List

import PySimpleGUI as sg
import pyautogui
from PySimpleGUI import Window, Button, BLUES

from api.p0_script_api_client import protocol0
from lib.decorators import throttle, gui_unique_window
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


@gui_unique_window
def show_message(message: str, auto_close_duration=None, background_color: Optional[ColorEnum] = None) -> Window:
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

    from api.midi_app import call_system_method

    t = Timer(auto_close_duration, partial(call_system_method, close_current_window))
    if GuiState.CURRENT_TIMER:
        GuiState.CURRENT_TIMER.cancel()
    GuiState.CURRENT_TIMER = t
    t.start()

    return window


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


@gui_unique_window
def show_select(question: str, options: List[str], vertical=True) -> None:

    layout = [
        [sg.Text(question, key="question")],
        [sg.Input(key="input", visible=False)],
    ]

    buttons: List[Button] = [sg.Button(
        option,
        key=option,
        enable_events=True,
        button_color=('white', BLUES[1] if i == 0 else BLUES[0])
    ) for i, option in enumerate(options)]
    if vertical:
        layout += [[button] for button in buttons]
    else:
        layout.append(buttons)

    window = sg.Window(
        "Select Window",
        layout,
        modal=True,
        return_keyboard_events=True,
        keep_on_top=True,
        no_titlebar=True,
        element_justification='c'
    )

    selected_option = options[0]

    def scroll_selected_option(go_next=True):
        nonlocal selected_option
        increment = 1 if go_next else -1
        index = (options.index(selected_option) + increment) % len(options)
        window[selected_option].update(button_color=('white', BLUES[0]))
        selected_option = options[index]
        window[selected_option].update(button_color=('white', BLUES[1]))

    def update_selected_option():
        window[selected_option].update(button_color=('white', BLUES[1]))

    while True:
        event, values = window.read()

        update_selected_option()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if isinstance(event, str):
            key = event.split(":")[0]
            if key == "Escape":
                break
            elif (key == "Right" and vertical is False) or (key == "Down" and vertical is True):
                scroll_selected_option(go_next=True)
            elif (key == "Left" and vertical is False) or (key == "Up" and vertical is True):
                scroll_selected_option(go_next=False)

            elif len(event) == 1 and ord(event) == 13:
                break

        if event in options:
            break

    window.close()
    protocol0.system_response(selected_option)
