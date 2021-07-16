from functools import partial

from lib.process import execute_cli_command
from server.p0_script_api_client import p0_script_api_client
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition


class SpeechRecognitionMain(AbstractSpeechRecognition):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = True
    USE_GUI = False

    def _setup_observers(self):
        super()._setup_observers()
        if self.SEND_SEARCH_TO_ABLETON:
            self.recognizer.subscribe(str, p0_script_api_client.search_track)
        if self.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            self.recognizer.subscribe(AbstractRecognizerNotFoundError, partial(execute_cli_command, "search_set_gui"))
