from gui.window.window import Window
from lib.enum.NotificationEnum import NotificationEnum


class WindowFactory():
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum, **k) -> Window:
        raise NotImplementedError
