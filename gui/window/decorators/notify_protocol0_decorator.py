from loguru import logger

from api.p0_system_api_client import system_client
from gui.window.decorators.window_decorator import WindowDecorator
from lib.patterns.observer.observer_mixin import ObserverMixin


class NotifyProtocol0Decorator(WindowDecorator, ObserverMixin):
    def display(self):
        self.window.display()
        self.sg_window.close()

    def update(self, data):
        logger.info(f"sending system response {data}")

        system_client.send_system_response(data)
