from abc import abstractmethod

from typing_extensions import Protocol

from sr.audio.speech_sound import SpeechSound
from sr.recognizer.recognizer_result import RecognizerResult


class RecognizerInterface(Protocol):
    @abstractmethod
    def process_speech_sound(self, speech_sound: SpeechSound) -> RecognizerResult:
        raise NotImplementedError

    @abstractmethod
    def load_model(self, sample_rate: int):
        raise NotImplementedError
