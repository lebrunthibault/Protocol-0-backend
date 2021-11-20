from loguru import logger

from gui.gui import show_message
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


def display_recognizer_result(recognizer_result: RecognizerResult):
    show_message(message=str(recognizer_result), auto_close_duration=1 if recognizer_result.error else 1,
                 background_color=recognizer_result.display_color)
