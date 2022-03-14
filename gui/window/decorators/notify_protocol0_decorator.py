from loguru import logger

from api.midi_server.p0_backend_api_client import backend_client
from gui.window.decorators.window_decorator import WindowDecorator
from lib.patterns.observer.observer_mixin import ObserverMixin


class NotifyProtocol0Decorator(WindowDecorator, ObserverMixin):
    def display(self):
        self.window.display()
        self.sg_window.close()

    def update(self, data):
        logger.info(f"sending backend response {data}")

        backend_client.send_backend_response(data)
