from gui.window.window import Window
from lib.enum.NotificationEnum import NotificationEnum


class WindowBuilder():
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum) -> Window:
        raise NotImplementedError
