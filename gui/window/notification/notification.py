import time

import PySimpleGUI as sg
import pyautogui
from loguru import logger

from gui.task_cache import TaskCache
from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


class Notification(Window):
    def __init__(
        self,
        message: str,
        background_color: ColorEnum,
        timeout: float = 0
    ):
        self._message = message
        background_color = background_color.hex_value
        self._timeout = timeout

        self._start_at = time.time()
        self._task_cache = TaskCache()

        self.sg_window = sg.Window("Notification message",
                                   layout=[[sg.Text(message, background_color=background_color)]],
                                   no_titlebar=True,
                                   use_default_focus=False,
                                   location=(pyautogui.size()[0] - (100 + 7 * len(message)), 10),
                                   background_color=background_color,
                                   keep_on_top=True,
                                   )

    def display(self, task_id: str):
        while True:
            self.sg_window.read(timeout=200)
            if self._timeout and time.time() - self._start_at > self._timeout:
                logger.info(f"window timeout closing {task_id}")
                break
            elif task_id in self._task_cache.revoked_tasks():
                logger.warning(f"window revoked closing {task_id}")
                break
        self.sg_window.close()
