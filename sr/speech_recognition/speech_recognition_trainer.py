import json
import os
from datetime import datetime
from typing import List

from loguru import logger

from lib.consts import PROJECT_ROOT
from lib.utils import filename_datetime
from sr.Recognizer import Recognizer, RecognizerStep
from sr.dictionary.TrackWordEnum import TrackWorkEnum
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition


class WordResult():
    def __init__(self, word):
        self.word = word
        self.count = 0

    def increment_count(self):
        self.count += 1


class TrainingSessionResult():
    def __init__(self):
        self._word_results: List[WordResult] = []

    def to_dict(self):
        return {word_result.word: word_result.count for word_result in self._word_results}

    def add_word(self, word: str):
        word_result = next((x for x in self._word_results if x.word == word), WordResult(word=word))
        word_result.increment_count()
        self._word_results.append(word_result)


class SpeechRecognitionTrainer(AbstractSpeechRecognition):
    FINAL_PROCESSING_STEP = RecognizerStep

    def __init__(self, target_word: str):
        super().__init__()
        self.target_word = target_word
        if not getattr(TrackWorkEnum, target_word.upper(), None):
            raise NameError(f"The word {target_word} does not exists in the word enum")

        directory = f"{PROJECT_ROOT}/sr/results/{target_word}"
        if not os.path.exists(directory):
            os.mkdir(directory)

        self.result_filename = f"{directory}/{filename_datetime()}.json"
        self.training_session_result = TrainingSessionResult()

    def _init_recognizers(self):
        self.recognizers = [
            Recognizer(model_name=self.REFERENCE_MODEL, sample_rate=self.mic.SAMPLE_RATE),
        ]

    def _process_result(self, word: str):
        self.training_session_result.add_word(word)
        logger.info(self.training_session_result)
        output = {
            "target_word": self.target_word,
            "datetime": datetime.now().isoformat(),
            "result": self.training_session_result.to_dict()
        }

        with open(self.result_filename, "w") as f:
            f.write(json.dumps(output))
