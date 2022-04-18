import PySimpleGUI as sg

from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


# centered notification
class Message(Window):
    def __init__(
        self,
        message: str,
        background_color: ColorEnum,
        title="P0 Message"
    ):
        background_color_hex = background_color.hex_value
        self.sg_window = sg.Window(title,
                                   layout=[[sg.Text(message, background_color=background_color_hex)]],
                                   return_keyboard_events=True,
                                   no_titlebar=True,
                                   use_default_focus=False,
                                   element_justification="c",
                                   background_color=background_color_hex,
                                   keep_on_top=True,
                                   )

    def display(self):
        self.focus()
        while True:
            event, values = self.sg_window.read()
            if self.is_event_escape(event) or self.is_event_enter(event):
                break

        self.sg_window.close()
