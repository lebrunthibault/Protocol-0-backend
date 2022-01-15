from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationError(Notification):
    def __init__(self, message: str):
        super(NotificationError, self).__init__(message=message, background_color=ColorEnum.ERROR, no_titlebar=False)
