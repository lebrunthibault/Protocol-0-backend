from gui.window.decorators.window_decorator import WindowDecorator
from gui.window.window import Window


class CloseWindowOnEndDecorator(WindowDecorator, Window):
    def __init__(self, window: Window):
        self.window = window
        self.sg_window = window.sg_window

    def display(self):
        self.window.display()
        self.sg_window.close()
