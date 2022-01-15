from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationWarning(Notification):
    def __init__(self, message: str):
        super(NotificationWarning, self).__init__(message=message, background_color=ColorEnum.WARNING)
