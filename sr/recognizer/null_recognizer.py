from sr.audio.recording import Recording
from sr.enums.recognizer_step_enum import RecognizerStepEnum
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.recognizer.recognizer import Recognizer, RecognizerResult


class NullRecognizer(Recognizer):
    def __init__(self):
        super().__init__(model=SpeechRecognitionModelEnum.MAIN_MODEL, sample_rate=0,
                         final_recognizer_step=RecognizerStepEnum.NO_PROCESSING)

    def process_recording(self, recording: Recording) -> RecognizerResult:
        return RecognizerResult(recording=recording)
