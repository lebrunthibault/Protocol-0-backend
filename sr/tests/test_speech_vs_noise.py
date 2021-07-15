from sr.audio.recording import Recording
from sr.audio.source.audio_file import AudioFile
from sr.config import Config
from sr.recognizer.null_recognizer import NullRecognizer
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition


class SpeechRecognitionTest(AbstractSpeechRecognition):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = False
    USE_GUI = False

    def __init__(self, source: AudioFile):
        super().__init__(source=source, recognizer=NullRecognizer())
        self.recordings = []
        self.recorder.subscribe(Recording, self.process_recording)

    def process_recording(self, recording: Recording):
        self.recordings.append(recording)


def test_speech_recognition():
    sr = SpeechRecognitionTest(source=AudioFile(f"{Config.TEST_DATA_DIRECTORY}/hello.wav"))
    sr.recognize()
    assert len(sr.recordings) == 1
