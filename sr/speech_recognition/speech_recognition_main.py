from loguru import logger
from server.p0_script_api_client import p0_script_api_client
from sr.recognizer.recognizer import RecognizerResult
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition


class SpeechRecognitionMain(AbstractSpeechRecognition):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = False
    USE_GUI = True

    def __init__(self):
        super().__init__()
        # self.recognizer = NullRecognizer()

    def _process_recognizer_result(self, recognizer_result: RecognizerResult):
        word = recognizer_result.word_enum.name
        self.emit(recognizer_result.word_enum)
        if self.SEND_SEARCH_TO_ABLETON:
            logger.info(f"sending search {word} to api")
            p0_script_api_client.search_track(search=word)
