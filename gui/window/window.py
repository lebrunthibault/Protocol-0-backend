from PySimpleGUI import Window


class Window():
    sg_window: Window

    def display(self):
        raise NotImplementedError
