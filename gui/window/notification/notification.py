import time
from typing import Optional

import PySimpleGUI as sg
import pyautogui
from loguru import logger

from gui.task_cache import TaskCache
from gui.window.window import Window
from lib.enum.ColorEnum import ColorEnum


class Notification(Window):
    def __init__(
        self, message: str, background_color: ColorEnum, centered: bool, timeout: float = 0
    ):
        self._message = message
        background_color_hex = background_color.hex_value
        self._timeout = timeout

        self._start_at = time.time()
        self._task_cache = TaskCache()

        kw = {}
        if not centered:
            kw["location"] = (pyautogui.size()[0] - (100 + 7 * len(message)), 10)

        self.sg_window = sg.Window(
            "Notification message",
            layout=[[sg.Text(message, background_color=background_color_hex)]],
            return_keyboard_events=True,
            no_titlebar=True,
            use_default_focus=False,
            background_color=background_color_hex,
            keep_on_top=True,
            **kw,
        )

    def display(self, task_id: Optional[str] = None):
        self.focus()
        while True:
            event, values = self.sg_window.read(timeout=200)

            if self.is_event_escape(event) or self.is_event_enter(event):
                break
            if self._timeout and time.time() - self._start_at > self._timeout:
                logger.info(f"window timeout closing {task_id}")
                break
            elif task_id is not None and task_id in self._task_cache.revoked_tasks():
                logger.warning(f"window revoked closing {task_id}")
                break

            if task_id is not None:
                self._task_cache.remove_revoked_task(task_id)

        self.sg_window.close()
