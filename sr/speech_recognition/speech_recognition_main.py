from functools import partial

from api.p0_script_api_client import p0_script_api_client
from lib.process import execute_cli_command
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.recognizer.recognizer import Recognizer
from sr.speech_recognition.speech_recognition import SpeechRecognition


class SpeechRecognitionMain(object):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = True

    @classmethod
    def recognize(cls):
        sr = SpeechRecognition(recognizer=Recognizer())
        if cls.SEND_SEARCH_TO_ABLETON:
            sr.recognizer.subscribe(str, p0_script_api_client.search_track)
        if cls.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            sr.recognizer.subscribe(AbstractRecognizerNotFoundError, partial(execute_cli_command, "search_set_gui"))

        sr.listen()
