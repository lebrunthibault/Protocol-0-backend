from typing import List

from PySimpleGUI import Button

from gui.window.select.select import Select


class SelectHorizontal(Select):
    def __init__(self, buttons: List[Button], *a, **k):
        buttons = [buttons]
        super(SelectHorizontal, self).__init__(buttons=buttons, *a, **k)
