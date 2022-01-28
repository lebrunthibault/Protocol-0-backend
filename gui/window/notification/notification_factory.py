from gui.window.decorators.auto_close_window_decorator import AutoCloseNotificationDecorator
from gui.window.notification.notification_error import NotificationError
from gui.window.notification.notification_info import NotificationInfo
from gui.window.notification.notification_warning import NotificationWarning
from gui.window.window import Window
from gui.window.window_factory import WindowFactory
from lib.enum.NotificationEnum import NotificationEnum


class NotificationFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO) -> Window:
        if notification_enum == NotificationEnum.INFO:
            notification = NotificationInfo(message=message)
        elif notification_enum == NotificationEnum.WARNING:
            notification = NotificationWarning(message=message)
        elif notification_enum == NotificationEnum.ERROR:
            notification = NotificationError(message=message)
        else:
            raise NotImplementedError

        if notification_enum != NotificationEnum.INFO:
            notification = AutoCloseNotificationDecorator(notification)

        return notification

    @classmethod
    def show_error(cls, message: str):
        cls.createWindow(message=message, notification_enum=NotificationEnum.ERROR).display()

