import sys

from loguru import logger

from gui.window.decorators.window_decorator import WindowDecorator
from lib.patterns.observer.observer_mixin import ObserverMixin
from protocol0.application.command.ProcessBackendResponseCommand import ProcessBackendResponseCommand


class NotifyProtocol0Decorator(WindowDecorator, ObserverMixin):
    def display(self):
        self.window.display()
        self.sg_window.close()

    def update(self, data):
        logger.info(f"sending backend response {data}")
        # so that the client is not created at boot time
        logger.info(sys.path)
        from api.client.p0_script_api_client import p0_script_client
        p0_script_client().dispatch(ProcessBackendResponseCommand(data))
