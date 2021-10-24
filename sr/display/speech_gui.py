import PySimpleGUI as sg
import pyautogui
from PySimpleGUI import POPUP_BUTTONS_NO_BUTTONS
from loguru import logger

from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


class SpeechGui(object):
    @classmethod
    def display_message(cls, message: str, auto_close_duration=1, background_color=None):
        sg.popup(message,
                 auto_close=True,
                 auto_close_duration=auto_close_duration,
                 no_titlebar=True,
                 location=(pyautogui.size()[0] - (80 + 6 * len(message)), 10),
                 background_color=background_color,
                 keep_on_top=True,
                 # non_blocking=True,
                 modal=False,
                 button_type=POPUP_BUTTONS_NO_BUTTONS,
                 )

    @classmethod
    def display_recognizer_result(cls, recognizer_result: RecognizerResult):
        cls.display_message(message=str(recognizer_result), auto_close_duration=1 if recognizer_result.error else 1,
                            background_color=recognizer_result.display_color)
