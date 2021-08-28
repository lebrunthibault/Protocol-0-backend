import operator
from enum import Enum
from functools import reduce
from os.path import dirname, realpath
from typing import Dict, List

from protocol0.enums.ActionEnum import ActionEnum
from protocol0.enums.TrackSearchKeywordEnum import TrackSearchKeywordEnum

from sr.enums.speech_command_enum import SpeechCommandEnum

root = dirname(realpath(__file__))


class SRConfig:
    WINDOW_TITLE = "speech"
    DEBUG = True
    USE_GUI = True
    EXPORT_RESULTS = False
    SR_ACTIVE = True
    WORD_ENUM_CLASSES = [
        ActionEnum,
        TrackSearchKeywordEnum,
        SpeechCommandEnum
    ]

    TEST_DATA_DIRECTORY = f"{root}\\tests\\data"
    TEST_DEBUG_DATA_DIRECTORY = f"{root}\\tests\\debug_data"
    TRAINING_SYNONYMS_DIRECTORY = f"{root}\\training\\synonyms"
    TRAINING_AUDIO_DIRECTORY = f"{root}\\training\\audio"
    SYNONYMS_PATH = f"{root}\\dictionary\\synonyms.py"
    KALDI_VOCABULARY_PATH = f"{root}\\grammar\\vocabulary.txt"

    @classmethod
    def word_enums(cls) -> List[Enum]:
        return reduce(operator.add, [list(enum_class) for enum_class in cls.WORD_ENUM_CLASSES])

    @classmethod
    def word_enums_dict(cls) -> Dict[str, Enum]:
        return {enum.name: enum for enum in cls.word_enums()}
