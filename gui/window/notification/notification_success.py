from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationSuccess(Notification):
    def __init__(self, message: str):
        super(NotificationSuccess, self).__init__(message=message, background_color=ColorEnum.SUCCESS)
