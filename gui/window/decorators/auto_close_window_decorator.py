from time import sleep

from gui.window.decorators.window_decorator import WindowDecorator
from gui.window.notification.notification import Notification


class AutoCloseNotificationDecorator(WindowDecorator, Notification):
    BASE_SECOND_DURATION = 2
    CHAR_SECOND_DURATION = 0.05

    def __init__(self, notification: Notification):
        self.window = notification

    def display(self):
        auto_close_duration = self.BASE_SECOND_DURATION + len(self.window.message) * self.CHAR_SECOND_DURATION

        self.window.display()

        sleep(auto_close_duration)
        self.window.sg_window.close()
