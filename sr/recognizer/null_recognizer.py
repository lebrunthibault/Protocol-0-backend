from sr.audio.speech_sound import SpeechSound
from sr.recognizer.recognizer_interface import RecognizerInterface
from sr.recognizer.recognizer_result import RecognizerResult


class NullRecognizer(RecognizerInterface):
    def process_speech_sound(self, speech_sound: SpeechSound) -> RecognizerResult:
        return RecognizerResult(speech_sound=speech_sound)

    def load_model(self, sample_rate: int):
        pass
