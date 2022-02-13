from functools import partial
from threading import Timer

from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum
from lib.window.window import focus_window


class NotificationError(Notification):
    WINDOW_NAME = "P0 Error"

    def __init__(self, message: str):
        super(NotificationError, self).__init__(message=message, background_color=ColorEnum.ERROR)
        self.sg_window.Title = self.WINDOW_NAME
        self.sg_window.NoTitleBar = False
        self.sg_window.Location = (None, None)
        self.sg_window.ElementJustification = "c"

    def display(self):
        # focus_window(self.WINDOW_NAME)
        event, values = self.sg_window.read()
        print(event, values)
        self.sg_window.close()
