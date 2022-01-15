from threading import Timer
from threading import Timer
from typing import Optional, List

import PySimpleGUI as sg
from PySimpleGUI import Button, BLUES

from api.p0_script_api_client import protocol0
from lib.decorators import gui_unique_window

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
