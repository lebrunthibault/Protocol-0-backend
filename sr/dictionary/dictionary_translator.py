import functools
from typing import Optional

from sr.dictionary.synonyms import speech_recognition_dictionary
from sr.enums.ableton_command_enum import AbletonCommandEnum


class DictionaryTranslator():
    @classmethod
    @functools.lru_cache()
    def _word_to_enum_mapping(cls):
        mapping = {}
        for enum in speech_recognition_dictionary.keys():
            for word in speech_recognition_dictionary[enum]:
                mapping[word] = enum

        return mapping

    @classmethod
    def translate_word(cls, word: str) -> Optional[AbletonCommandEnum]:
        direct_correspondence = getattr(AbletonCommandEnum, word.upper(), None)
        if direct_correspondence:
            return direct_correspondence
        else:
            return cls._word_to_enum_mapping().get(word, None)
