from typing import Optional

import PySimpleGUI as sg

from api.p0_script_api_client import protocol0
from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


class Prompt(Window):
    def __init__(
        self,
        message: str,
        background_color: Optional[ColorEnum],
        no_titlebar=True
    ):
        background_color = background_color.hex_value if background_color else None
        ok = False
        layout = [
            [sg.Text(message, key="question", background_color=background_color)],
            [sg.Input(key="input", visible=False)],
            [sg.Button("ok", key="ok")],
        ]
        self.sg_window = sg.Window(
            "Dialog Window",
            layout,
            modal=True,
            return_keyboard_events=True,
            keep_on_top=True,
            no_titlebar=True,
            background_color=background_color,
            element_justification='c'
        )

    def display(self):
        while True:
            event, values = self.sg_window.read()
            print(event, type(event), values)
            if event == "Exit" or event == sg.WIN_CLOSED or event.split(":")[0] == "Escape":
                break

            if event == "ok" or (len(event) == 1 and ord(event) == 13):
                ok = True
                break

        self.sg_window.close()
        protocol0.system_response(ok)
