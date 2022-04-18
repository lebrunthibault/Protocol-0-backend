from gui.window.notification.notification import Notification
from gui.window.window_factory import WindowFactory
from lib.enum.ColorEnum import ColorEnum
from lib.enum.NotificationEnum import NotificationEnum


class NotificationFactory(WindowFactory):
    BASE_SECOND_DURATION = 2
    CHAR_SECOND_DURATION = 0.05

    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO, centered=False) -> Notification:
        auto_close_duration = cls.BASE_SECOND_DURATION + len(message) * cls.CHAR_SECOND_DURATION

        if notification_enum == NotificationEnum.INFO:
            return Notification(message=message, background_color=ColorEnum.INFO, centered=centered, timeout=auto_close_duration)
        elif notification_enum == NotificationEnum.SUCCESS:
            return Notification(message=message, background_color=ColorEnum.SUCCESS, centered=centered, timeout=auto_close_duration)
        elif notification_enum == NotificationEnum.WARNING:
            return Notification(message=message, background_color=ColorEnum.WARNING, centered=centered, timeout=auto_close_duration)
        elif notification_enum == NotificationEnum.ERROR:
            return Notification(message=message, background_color=ColorEnum.ERROR, centered=centered)
        else:
            raise NotImplementedError("cannot find notification class for enum %s" % notification_enum)
