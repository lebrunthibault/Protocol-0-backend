from gui.window.window import Window


class WindowDecorator(Window):
    def __init__(self, window: Window):
        self.window = window
        self.sg_window = window.sg_window

    def display(self):
        raise NotImplementedError
