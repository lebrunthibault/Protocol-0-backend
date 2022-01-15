from api.p0_script_api_client import protocol0
from gui.window.decorators.window_decorator import WindowDecorator
from gui.window.window import Window
from lib.patterns.observer.Observer import Observer


class NotifyProtocol0Decorator(WindowDecorator, Observer, Window):
    def __init__(self, window: Window):
        self.window = window
        self.sg_window = window.sg_window
        self.window.attach(self)

    def display(self):
        self.window.display()
        self.sg_window.close()

    def update(self, data):
        protocol0.system_response(data)
