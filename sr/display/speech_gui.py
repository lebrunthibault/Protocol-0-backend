from typing import Optional, Any

import PySimpleGUI as sg
import pyautogui
from lib.observable import Observable
from loguru import logger

logger = logger.opt(colors=True)


class SpeechGui(Observable):
    RUNNING = True

    def __init__(self):
        super().__init__()
        self.window: Optional[sg.Window] = None

    def process_message(self, message: Any):
        self.window.TKroot.focus_force()  # force this window to have focus
        self.window["logs"].update(str(message))

    def create_window(self):
        layout = [[sg.Text('logs', key='logs', size=(200, 30), pad=(10, 8))],
                  [sg.Quit(size=(30, 30))]]

        self.window = sg.Window(
            'Speech logs',
            layout,
            # no_titlebar=True,
            location=(pyautogui.size()[0] - 270, 20),
            # location=(pyautogui.size()[0] - 250, 20),
            finalize=True,
            auto_size_text=False,
            size=(246, 50)
        )

        while True:  # Event Loop
            # Please try and use as high of a timeout value as you can
            event, values = self.window.read(timeout=1000)

            # if user closed the window using X or clicked Quit button
            if event in (sg.WIN_CLOSED, 'Quit') or not self.RUNNING:
                break

        logger.info("closing GUI window")
        self.window.close()
        self.emit("exit")

    def exit(self):
        if self.RUNNING:
            logger.info("exiting in GUI")
            self.RUNNING = False
