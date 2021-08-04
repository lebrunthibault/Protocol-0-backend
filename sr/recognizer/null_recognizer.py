from sr.audio.short_sound import ShortSound
from sr.recognizer.recognizer_interface import RecognizerInterface


class NullRecognizer(RecognizerInterface):
    def handle_recording(self, recording: ShortSound) -> None:
        self.emit(recording)

    def load_model(self, sample_rate: int):
        pass
