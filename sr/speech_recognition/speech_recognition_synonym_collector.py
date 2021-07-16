import json
import os
from datetime import datetime
from typing import List

from lib.utils import filename_datetime
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.enums.recognizer_step_enum import RecognizerStepEnum
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.recognizer.recognizer import Recognizer
from sr.recognizer.recognizer_result import RecognizerResult
from sr.speech_recognition.abstract_speech_recognition import AbstractSpeechRecognition
from sr.sr_config import SRConfig


class WordResult:
    def __init__(self, word):
        self.word = word
        self.count = 0

    def increment_count(self):
        self.count += 1


class TrainingSessionResult:
    def __init__(self, target_word: str):
        self._target_word = target_word
        self._word_results: List[WordResult] = []
        result_directory = f"{SRConfig.TRAINING_SYNONYMS_DIRECTORY}/{target_word}"
        if not os.path.exists(result_directory):
            os.mkdir(result_directory)

        self._result_filename = f"{result_directory}/{filename_datetime()}.json"

    def to_dict(self):
        return {word_result.word: word_result.count for word_result in self._word_results}

    def add_word(self, word: str):
        word_result = next((x for x in self._word_results if x.word == word), WordResult(word=word))
        word_result.increment_count()
        self._word_results.append(word_result)

    def export(self):
        output = {"target_word": self._target_word, "datetime": datetime.now().isoformat(), "result": self.to_dict()}

        with open(self._result_filename, "w") as f:
            f.write(json.dumps(output))


class SpeechRecognitionSynonymCollector(AbstractSpeechRecognition):
    def __init__(self, target_word: str):
        super().__init__()
        assert target_word in AbletonCommandEnum.words(), "word should be in the word enum"
        self.target_word = target_word
        self.training_session_result = TrainingSessionResult(target_word=target_word)
        self.recognizer = Recognizer(
            model=SpeechRecognitionModelEnum.REFERENCE_MODEL,
            sample_rate=self.recorder.sample_rate,
            final_recognizer_step=RecognizerStepEnum.RECOGNIZER,
        )
        self.recognizer.subscribe(RecognizerResult, self._process_recognizer_result)

    def _process_recognizer_result(self, recognizer_result: RecognizerResult):
        self.training_session_result.add_word(recognizer_result.word)
        self.training_session_result.export()
