from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationInfo(Notification):
    def __init__(self, message: str):
        super(NotificationInfo, self).__init__(message=message, background_color=ColorEnum.INFO)
