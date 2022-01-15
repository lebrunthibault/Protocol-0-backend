from PySimpleGUI import Window

from lib.patterns.observer.observable import Observable


class Window(Observable):
    sg_window: Window

    def display(self):
        raise NotImplementedError
