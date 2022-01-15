from loguru import logger

from gui.window.notification.notification_builder import NotificationBuilder
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


def display_recognizer_result(recognizer_result: RecognizerResult):
    NotificationBuilder.createWindow(
        message=str(recognizer_result),
        notification_enum=recognizer_result.notification_type
    ).display()
