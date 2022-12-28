from gui.window.window import Window
from lib.enum.notification_enum import NotificationEnum


class WindowFactory:
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum, **k) -> Window:
        raise NotImplementedError
