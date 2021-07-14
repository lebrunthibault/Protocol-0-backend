from sr.audio.recording import Recording
from sr.recognizer.recognizer import Recognizer, RecognizerResult


class NullRecognizer(Recognizer):
    def __init__(self):
        pass

    def process_recording(self, recording: Recording) -> RecognizerResult:
        return RecognizerResult()
