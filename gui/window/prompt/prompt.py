from typing import Optional

import PySimpleGUI as sg

from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


class Prompt(Window):
    def __init__(
        self,
        message: str,
        background_color: Optional[ColorEnum],
        no_titlebar=True
    ):
        super(Prompt, self).__init__()
        background_color = background_color.hex_value if background_color else None
        layout = [
            [sg.Text(message, key="question", background_color=background_color)],
            [sg.Input(key="input", visible=False)],
            [sg.Button("yes", key="yes"), sg.Button("no", key="no")]
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
            if event == "no" or event == "Exit" or event == sg.WIN_CLOSED or event.split(":")[0] == "Escape":
                self.notify(False)
                break

            if event == "yes" or (len(event) == 1 and ord(event) == 13):
                self.notify(True)
                break
