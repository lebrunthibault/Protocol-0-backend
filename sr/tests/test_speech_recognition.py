from sr.config import Config
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition

from speech_recognition.audio_source.AudioFile import AudioFile


class SpeechRecognitionTest(AbstractSpeechRecognition):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = False
    USE_GUI = False


def test_speech_recognition():
    SpeechRecognitionTest(source=AudioFile(f"{Config.TEST_DATA_DIRECTORY}/hello.wav")).recognize()
