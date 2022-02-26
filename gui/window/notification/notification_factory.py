from gui.window.decorators.auto_close_window_decorator import AutoCloseNotificationDecorator
from gui.window.notification.notification import Notification
from gui.window.window_factory import WindowFactory
from lib.enum.ColorEnum import ColorEnum
from lib.enum.NotificationEnum import NotificationEnum


class NotificationFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO) -> Notification:
        if notification_enum == NotificationEnum.INFO:
            notification = Notification(message=message, background_color=ColorEnum.INFO)
        elif notification_enum == NotificationEnum.SUCCESS:
            notification = Notification(message=message, background_color=ColorEnum.SUCCESS)
        elif notification_enum == NotificationEnum.WARNING:
            notification = Notification(message=message, background_color=ColorEnum.WARNING)
        elif notification_enum == NotificationEnum.ERROR:
            notification = Notification(message=message, background_color=ColorEnum.ERROR)
        else:
            raise NotImplementedError("cannot find notification class for enum %s" % notification_enum)

        if notification_enum != NotificationEnum.ERROR:
            notification = AutoCloseNotificationDecorator(notification)

        return notification
