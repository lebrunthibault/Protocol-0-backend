from gui.window.notification.notification import Notification
from gui.window.window_factory import WindowFactory
from lib.enum.notification_enum import NotificationEnum


class NotificationFactory(WindowFactory):
    BASE_SECOND_DURATION = 2
    CHAR_SECOND_DURATION = 0.05

    @classmethod
    def createWindow(
        cls,
        message: str,
        notification_enum: NotificationEnum = NotificationEnum.INFO,
        centered=False,
    ) -> Notification:
        auto_close_duration = cls.BASE_SECOND_DURATION + len(message) * cls.CHAR_SECOND_DURATION
        return Notification(
            message=message,
            background_color=notification_enum.color,
            centered=centered,
            timeout=auto_close_duration,
            autofocus=notification_enum == NotificationEnum.ERROR,
        )

    @classmethod
    def show_error(cls, message: str):
        cls.createWindow(message=message, notification_enum=NotificationEnum.ERROR).display()
