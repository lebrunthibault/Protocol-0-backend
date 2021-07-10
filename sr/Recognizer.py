import json
from os.path import dirname
from typing import Optional

from loguru import logger

logger = logger.opt(colors=True)

from speech_recognition.audio_data.AudioData import AudioData
from vosk import KaldiRecognizer, Model

from lib.consts import PROJECT_ROOT
from lib.observable import Observable
from sr.dictionary.DictionaryManager import DictionaryManager
from sr.dictionary.DictionaryTranslator import DictionaryTranslator


class RecognizerResult():
    def __init__(self):
        self.raw_result: Optional[str] = None
        self.word_enum: Optional[str] = None


class RecognizerStep():
    RECOGNIZER = "RECOGNIZER"
    DICTIONARY = "DICTIONARY"


class Recognizer(Observable):
    DEBUG = False

    def __init__(self, model_name: str, sample_rate: int, use_word_list=False):
        self.name = model_name
        self.sample_rate = sample_rate
        self.use_word_list = use_word_list
        self._recognizer: Optional[KaldiRecognizer] = None
        self.dictionary_translator = DictionaryTranslator()

        self._load()

    def _load(self):
        logger.info(f"loading model {self.name}")
        model = Model(
            f"{PROJECT_ROOT}/sr/models/model_{self.name}")
        logger.info(f"model loaded")
        args = [model, self.sample_rate]
        if self.name != "p0" and self.use_word_list:
            args.append(json.dumps(DictionaryManager.get_word_list()))

        self._recognizer = KaldiRecognizer(*args)
        self._recognizer.SetWords(True)

    def process_audio_phrase(self, audio: AudioData) -> RecognizerResult:
        self._recognizer.AcceptWaveform(audio.frame_data)
        kaldi_result = json.loads(self._recognizer.FinalResult())

        if self.DEBUG:
            processing_duration = time.time() - audio.recording.end_at
            logger.info(f"recording duration <yellow>{audio.recording.duration:.2f}s</>")
            logger.info(f"processing duration <yellow>{processing_duration:.2f}s</>")
            logger.info(f"result: {kaldi_result}")
            full_result = json.loads(self._recognizer.Result())
            partial_result = json.loads(self._recognizer.PartialResult())
            logger.info(f"full_result: {full_result}")
            logger.info(f"partial_result: {partial_result}")

        result = RecognizerResult()

        word = kaldi_result["text"]
        if not word:
            return result

        logger.info(f"Got : <green>{word}</>")
        result.raw_result = word

        return self._process_result(result)

    def _process_result(self, result: RecognizerResult) -> RecognizerResult:
        word_clean = result.raw_result.replace("[unk]", "").strip()
        word_enum = self.dictionary_translator.translate_word(word=word_clean)
        if word_enum:
            result.word_enum = word_enum

        return result
