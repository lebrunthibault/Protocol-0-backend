from sr.recognizer.Recognizer import Recognizer, RecognizerResult

from speech_recognition.audio_data.Recording import Recording


class NullRecognizer(Recognizer):
    def __init__(self):
        pass

    def process_recording(self, recording: Recording) -> RecognizerResult:
        return RecognizerResult()
