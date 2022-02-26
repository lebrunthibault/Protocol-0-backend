from functools import partial
from threading import Timer
from typing import Optional

from PySimpleGUI import Window as SgWindow
from loguru import logger

from lib.patterns.observer.subject_mixin import SubjectMixin
from lib.window.window import focus_window


class Window(SubjectMixin):
    def __init__(self):
        self.sg_window: Optional[SgWindow] = None

    def display(self):
        raise NotImplementedError

    def focus(self):
        logger.info(self.sg_window.Title)
        if self.sg_window.Title is None:
            return
        for interval in (0.5, 1):
            Timer(interval, partial(focus_window, self.sg_window.Title)).start()

    def is_event_escape(self, event):
        return event == "Exit" or event.split(":")[0] == "Escape"

    def is_event_enter(self, event):
        return len(event) == 1 and ord(event) == 13

