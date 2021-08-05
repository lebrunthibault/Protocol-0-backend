import json
import time
from typing import Optional, Union

from loguru import logger
from vosk import KaldiRecognizer, Model

from config import PROJECT_ROOT
from sr.audio.speech_sound import SpeechSound
from sr.dictionary.dictionary_manager import DictionaryManager
from sr.dictionary.dictionary_translator import get_word_enum_from_dictionary
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.errors.dictionary_not_found_error import DictionaryNotFoundError
from sr.errors.recognizer_not_found_error import RecognizerNotFoundError
from sr.recognizer.recognizer_interface import RecognizerInterface
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


class Recognizer(RecognizerInterface):
    DEBUG = False

    def __init__(
        self,
        model: SpeechRecognitionModelEnum = SpeechRecognitionModelEnum.MAIN_MODEL,
        use_word_list=False
    ):
        super().__init__()
        self._model_name: str = model.value
        self._use_word_list = use_word_list
        self._recognizer: Optional[KaldiRecognizer] = None
        self.start_processing_at: Optional[float] = None

    def load_model(self, sample_rate: int):
        logger.info(f"loading model {self._model_name}")
        model = Model(f"{PROJECT_ROOT}/sr/models/model_{self._model_name}")
        args = [model, sample_rate]
        if self._model_name != "p0" and self._use_word_list:
            args.append(json.dumps(DictionaryManager.get_word_list()))

        self._recognizer = KaldiRecognizer(*args)
        self._recognizer.SetWords(True)

    def process_speech_sound(self, speech_sound: SpeechSound) -> Union[
        RecognizerResult, AbstractRecognizerNotFoundError]:
        self.start_processing_at = time.time()

        self._recognizer.AcceptWaveform(speech_sound.raw_data)
        if self.DEBUG:
            self._print_recognizer_info()

        word = json.loads(self._recognizer.FinalResult())["text"]
        clean_word = word.replace("[unk]", "").strip()
        logger.info(f"Got word: <green>{clean_word}</>")

        if not clean_word:
            return RecognizerNotFoundError()

        try:
            word_enum = get_word_enum_from_dictionary(word=clean_word)
        except DictionaryNotFoundError as e:
            return e

        logger.info(f"Found word in dictionary: <green>{word_enum}</>")

        return RecognizerResult(word=word, word_enum=word_enum)

    def _print_recognizer_info(self):
        kaldi_result = json.loads(self._recognizer.FinalResult())
        processing_duration = time.time() - self.start_processing_at
        logger.info(f"processing duration <yellow>{processing_duration:.2f}s</>")
        logger.info(f"result: {kaldi_result}")
        full_result = json.loads(self._recognizer.Result())
        partial_result = json.loads(self._recognizer.PartialResult())
        logger.info(f"full_result: {full_result}")
        logger.info(f"partial_result: {partial_result}")
