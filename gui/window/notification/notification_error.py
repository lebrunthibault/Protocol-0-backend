import PySimpleGUI as sg

from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationError(Notification):
    def __init__(self, message: str):
        super(NotificationError, self).__init__(message=message, background_color=ColorEnum.ERROR)
        self.sg_window.Title = "Error"
        self.sg_window.NoTitleBar = False
        self.sg_window.Location = (None, None)
        self.sg_window.ElementJustification = "c"

    def display(self):
        while True:
            event, values = self.sg_window.read()

            if event == "Exit" or event == sg.WIN_CLOSED:
                break
