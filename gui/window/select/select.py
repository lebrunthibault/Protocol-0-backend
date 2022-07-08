from typing import List, Tuple

import PySimpleGUI as sg
from PySimpleGUI import Button, BLUES

from gui.window.window import Window


class Select(Window):
    def __init__(
        self, message: str, options: List, buttons: List[List[Button]], arrow_keys: Tuple[str, str]
    ):
        layout = [
            [sg.Text(message, key="question")],
            [sg.Input(key="input", visible=False)],
            *buttons,
        ]
        self.arrow_keys = arrow_keys

        self.sg_window = sg.Window(
            "Select Window",
            layout,
            modal=True,
            return_keyboard_events=True,
            keep_on_top=True,
            no_titlebar=True,
            element_justification="c",
        )
        self.options = options
        self.selected_option = options[0]

    def display(self):
        self.focus()
        while True:
            event, values = self.sg_window.read()

            if self.is_event_escape(event) or self.is_event_enter(event):
                break

            if isinstance(event, str):
                key = event.split(":")[0]
                if key in self.arrow_keys:
                    self._scroll_selected_option(go_next=key == self.arrow_keys[1])
                elif event in self.options:
                    self.selected_option = event
                    break

        self.sg_window.close()
        self.notify(self.selected_option)

    def _scroll_selected_option(self, go_next=True):
        increment = 1 if go_next else -1
        index = (self.options.index(self.selected_option) + increment) % len(self.options)
        self.sg_window[self.selected_option].update(button_color=("white", BLUES[0]))
        self.selected_option = self.options[index]
        self.sg_window[self.selected_option].update(button_color=("white", BLUES[1]))
