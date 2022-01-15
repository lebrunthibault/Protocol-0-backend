from loguru import logger

from gui.window.notification.notification_factory import NotificationFactory
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


def display_recognizer_result(recognizer_result: RecognizerResult):
    NotificationFactory.createWindow(
        message=str(recognizer_result),
        notification_enum=recognizer_result.notification_type
    ).display()
