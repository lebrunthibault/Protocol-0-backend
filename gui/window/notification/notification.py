import PySimpleGUI as sg
import pyautogui

from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


class Notification(Window):
    def __init__(
        self,
        message: str,
        background_color: ColorEnum
    ):
        super(Notification, self).__init__()
        background_color = background_color.hex_value
        self.message = message

        self.sg_window = sg.Window("Message window",
                                   layout=[[sg.Text(message, background_color=background_color)]],
                                   no_titlebar=True,
                                   use_default_focus=False,
                                   location=(pyautogui.size()[0] - (100 + 7 * len(message)), 10),
                                   background_color=background_color,
                                   keep_on_top=True,
                                   )

    def display(self):
        self.sg_window.read(timeout=0)
