from loguru import logger

from gui.celery import notification_window
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


def display_recognizer_result(recognizer_result: RecognizerResult):
    notification_window.delay(str(recognizer_result), recognizer_result.notification_type)
