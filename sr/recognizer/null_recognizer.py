from lib.observable import Observable
from sr.audio.recording import Recording
from sr.recognizer.recognizer_interface import RecognizerInterface


class NullRecognizer(Observable, RecognizerInterface):
    def handle_recording(self, recording: Recording) -> None:
        self.emit(recording)
