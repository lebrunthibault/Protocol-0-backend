import json
import time
from typing import Optional

from loguru import logger
from vosk import KaldiRecognizer, Model

from sr.audio.speech_sound import SpeechSound
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.errors.dictionary_not_found_error import DictionaryNotFoundError
from sr.errors.recognizer_not_found_error import RecognizerNotFoundError
from sr.recognizer.recognizer_interface import RecognizerInterface
from sr.recognizer.recognizer_result import RecognizerResult
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


class Recognizer(RecognizerInterface):
    DEBUG = False

    def __init__(
        self,
        model: SpeechRecognitionModelEnum = SpeechRecognitionModelEnum.MAIN_MODEL
    ):
        super().__init__()
        self._model_name: str = model.value
        self._recognizer: Optional[KaldiRecognizer] = None
        self.start_processing_at: Optional[float] = None

    def load_model(self, sample_rate: int):
        logger.info(f"loading model {self._model_name}")
        model = Model(f"{SRConfig.PROJECT_ROOT}/models/model_{self._model_name}")
        args = [model, sample_rate]

        self._recognizer = KaldiRecognizer(*args)
        self._recognizer.SetWords(True)

    def process_speech_sound(self, speech_sound: SpeechSound) -> RecognizerResult:
        self.start_processing_at = time.time()

        self._recognizer.AcceptWaveform(speech_sound.raw_data)
        if self.DEBUG:
            self._print_recognizer_info()

        word = json.loads(self._recognizer.FinalResult())["text"]
        clean_word = word.replace("[unk]", "").strip().upper()
        logger.info(f"Got word: <green>{clean_word}</>")

        # only accept single words
        if not clean_word or " " in clean_word:
            return RecognizerResult(speech_sound=speech_sound, error=RecognizerNotFoundError())

        if clean_word not in SRConfig.word_enums_dict():
            return RecognizerResult(speech_sound=speech_sound, error=DictionaryNotFoundError())

        word_enum = SRConfig.word_enums_dict()[clean_word]

        logger.info(f"Found word in dictionary: <green>{word_enum}</>")

        return RecognizerResult(speech_sound=speech_sound, word=word, word_enum=word_enum)

    def _print_recognizer_info(self):
        kaldi_result = json.loads(self._recognizer.FinalResult())
        processing_duration = time.time() - self.start_processing_at
        logger.info(f"processing duration <yellow>{processing_duration:.2f}s</>")
        logger.info(f"result: {kaldi_result}")
        full_result = json.loads(self._recognizer.Result())
        partial_result = json.loads(self._recognizer.PartialResult())
        logger.info(f"full_result: {full_result}")
        logger.info(f"partial_result: {partial_result}")
