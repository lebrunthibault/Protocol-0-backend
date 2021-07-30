import functools
from typing import Optional

from loguru import logger

from sr.dictionary.synonyms import speech_recognition_dictionary
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.errors.dictionary_not_found_error import DictionaryNotFoundError
from sr.recognizer.recognizer_result import RecognizerResult


class DictionaryTranslator:
    @classmethod
    @functools.lru_cache()
    def _word_to_enum_mapping(cls):
        mapping = {}
        for enum in speech_recognition_dictionary.keys():
            for word in speech_recognition_dictionary[enum]:
                mapping[word] = enum

        return mapping

    @classmethod
    def _translate_word(cls, word: str) -> Optional[AbletonCommandEnum]:
        direct_correspondence = getattr(AbletonCommandEnum, word.upper(), None)
        if direct_correspondence:
            return direct_correspondence
        else:
            return cls._word_to_enum_mapping().get(word, None)

    @classmethod
    def process_recognizer_result(cls, recognizer_result: RecognizerResult) -> None:
        word_enum = cls._translate_word(word=recognizer_result.word)
        if not word_enum:
            raise DictionaryNotFoundError()

        logger.success(f"Found word enum: {word_enum.value}")
        recognizer_result.word_enum = word_enum
