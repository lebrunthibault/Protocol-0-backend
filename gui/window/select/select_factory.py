from typing import List

import PySimpleGUI as sg
from PySimpleGUI import Button, BLUES

from gui.window.decorators.close_window_on_end_decorator import CloseWindowOnEndDecorator
from gui.window.decorators.notify_protocol0_decorator import NotifyProtocol0Decorator
from gui.window.select.select_horizontal import SelectHorizontal
from gui.window.select.select_vertical import SelectVertical
from gui.window.window import Window
from gui.window.window_factory import WindowFactory


class SelectFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, options: List[str], vertical=True) -> Window:
        buttons = cls._create_buttons(options=options)
        if vertical:
            select = SelectVertical(message=message, options=options, buttons=buttons, arrow_keys=["Down", "Up"])
        else:
            select = SelectHorizontal(message=message, options=options, buttons=buttons, arrow_keys=["Left", "Right"])

        window = CloseWindowOnEndDecorator(select)
        window = NotifyProtocol0Decorator(window)
        select.attach(window)
        return window

    @classmethod
    def _create_buttons(self, options: List[str]) -> List[Button]:
        return [sg.Button(
            option,
            key=option,
            enable_events=True,
            button_color=('white', BLUES[1] if i == 0 else BLUES[0])
        ) for i, option in enumerate(options)]
