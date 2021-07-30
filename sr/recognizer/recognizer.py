import json
import time
from typing import Optional

from loguru import logger
from vosk import KaldiRecognizer, Model

from config import PROJECT_ROOT
from lib.observable import Observable
from sr.audio.recording import Recording
from sr.dictionary.dictionary_manager import DictionaryManager
from sr.dictionary.dictionary_translator import DictionaryTranslator
from sr.enums.recognizer_step_enum import RecognizerStepEnum
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.errors.dictionary_not_found_error import DictionaryNotFoundError
from sr.errors.recognizer_not_found_error import RecognizerNotFoundError
from sr.recognizer.recognizer_interface import RecognizerInterface
from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


class Recognizer(Observable, RecognizerInterface):
    DEBUG = False

    def __init__(
        self,
        model: SpeechRecognitionModelEnum = SpeechRecognitionModelEnum.MAIN_MODEL,
        use_word_list=False,
        final_recognizer_step: RecognizerStepEnum = RecognizerStepEnum.DICTIONARY,
    ):
        super().__init__()
        self._model_name: str = model.value
        self._use_word_list = use_word_list
        self._recognizer: Optional[KaldiRecognizer] = None
        self.final_recognizer_step = final_recognizer_step
        self.start_processing_at: Optional[float] = None

    def load_model(self, sample_rate: int):
        logger.info(f"loading model {self._model_name}")
        model = Model(f"{PROJECT_ROOT}/sr/models/model_{self._model_name}")
        args = [model, sample_rate]
        if self._model_name != "p0" and self._use_word_list:
            args.append(json.dumps(DictionaryManager.get_word_list()))

        self._recognizer = KaldiRecognizer(*args)
        self._recognizer.SetWords(True)

    def handle_recording(self, recording: Recording) -> None:
        self.start_processing_at = time.time()

        self._recognizer.AcceptWaveform(recording.raw_data)
        if self.DEBUG:
            self._print_recognizer_info()

        word = json.loads(self._recognizer.FinalResult())["text"]
        recognizer_result = RecognizerResult(word=word)
        logger.info(f"Got word: <green>{recognizer_result.word}</>")

        if not recognizer_result.word:
            self.emit(RecognizerNotFoundError())
            return

        if self.final_recognizer_step == RecognizerStepEnum.DICTIONARY:
            self._get_word_enum_from_result(recognizer_result=recognizer_result)

        self.emit(recognizer_result)
        self.emit(str(recognizer_result))

    def _get_word_enum_from_result(self, recognizer_result: RecognizerResult) -> None:
        word_clean = recognizer_result.word.replace("[unk]", "").strip()
        word_enum = DictionaryTranslator.translate_word(word=word_clean)
        if not word_enum:
            self.emit(DictionaryNotFoundError())
            return

        logger.success(f"Found word enum: {word_enum.value}")
        recognizer_result.word_enum = word_enum

    def _print_recognizer_info(self):
        kaldi_result = json.loads(self._recognizer.FinalResult())
        processing_duration = time.time() - self.start_processing_at
        logger.info(f"processing duration <yellow>{processing_duration:.2f}s</>")
        logger.info(f"result: {kaldi_result}")
        full_result = json.loads(self._recognizer.Result())
        partial_result = json.loads(self._recognizer.PartialResult())
        logger.info(f"full_result: {full_result}")
        logger.info(f"partial_result: {partial_result}")
