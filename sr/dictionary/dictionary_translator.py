import functools
from typing import Optional, Dict

from sr.dictionary.synonyms import speech_recognition_dictionary
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.errors.dictionary_not_found_error import DictionaryNotFoundError


@functools.lru_cache()
def _word_to_enum_mapping() -> Dict[str, AbletonCommandEnum]:
    mapping = {}
    for enum in speech_recognition_dictionary.keys():
        for word in speech_recognition_dictionary[enum]:
            mapping[word] = enum

    return mapping


def get_word_enum_from_dictionary(word: str) -> Optional[AbletonCommandEnum]:
    direct_correspondence = getattr(AbletonCommandEnum, word.upper(), None)
    if direct_correspondence:
        return direct_correspondence
    else:
        try:
            return _word_to_enum_mapping()[word]
        except KeyError:
            raise DictionaryNotFoundError()
