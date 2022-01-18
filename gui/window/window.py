from typing import Optional

from lib.patterns.observer.subject_mixin import SubjectMixin
from PySimpleGUI import Window as SgWindow


class Window(SubjectMixin):
    def __init__(self):
        self.sg_window: Optional[SgWindow] = None

    def display(self):
        raise NotImplementedError
