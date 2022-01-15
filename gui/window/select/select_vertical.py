from typing import List

from PySimpleGUI import Button

from gui.window.select.select import Select


class SelectVertical(Select):
    def __init__(self, buttons: List[Button], *a, **k):
        buttons = [[button] for button in buttons]
        super(SelectVertical, self).__init__(buttons=buttons, *a, **k)
