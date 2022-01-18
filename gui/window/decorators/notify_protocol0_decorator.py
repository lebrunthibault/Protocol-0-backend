from api.p0_script_api_client import protocol0
from gui.window.decorators.window_decorator import WindowDecorator
from lib.patterns.observer.observer_mixin import ObserverMixin


class NotifyProtocol0Decorator(WindowDecorator, ObserverMixin):
    def display(self):
        self.window.display()
        self.sg_window.close()

    def update(self, data):
        protocol0.system_response(data)
