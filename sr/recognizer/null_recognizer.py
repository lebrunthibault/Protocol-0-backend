from sr.audio.speech_sound import SpeechSound
from sr.recognizer.recognizer_interface import RecognizerInterface


class NullRecognizer(RecognizerInterface):
    def process_speech_sound(self, speech_sound: SpeechSound) -> str:
        return "NullRecognizer"

    def load_model(self, sample_rate: int):
        pass
