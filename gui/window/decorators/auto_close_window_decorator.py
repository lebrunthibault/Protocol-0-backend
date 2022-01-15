from functools import partial
from threading import Timer

from gui.window.decorators.window_decorator import WindowDecorator
from gui.window.notification.notification import Notification
from gui.window.window_registry import WindowRegistry


class AutoCloseNotificationDecorator(WindowDecorator, Notification):
    BASE_SECOND_DURATION = 2
    CHAR_SECOND_DURATION = 0.05

    def __init__(self, notification: Notification):
        self.notification = notification
        self.sg_window = notification.sg_window

    def display(self):
        auto_close_duration = self.BASE_SECOND_DURATION + len(self.notification.message) * self.CHAR_SECOND_DURATION

        self.notification.display()

        from api.midi_app import call_system_method

        t = Timer(auto_close_duration, partial(call_system_method, WindowRegistry.close_current_window))
        t.start()
