from typing import Optional

from sr.dictionary.TrackWordEnum import TrackWorkEnum
from sr.dictionary.synonyms import speech_recognition_dictionary


class DictionaryTranslator():
    def __init__(self):
        self.dictionary = speech_recognition_dictionary
        self._word_to_enum_mapping = self._create_word_to_enum_mapping()

    def _create_word_to_enum_mapping(self):
        mapping = {}
        for enum in speech_recognition_dictionary.keys():
            for word in speech_recognition_dictionary[enum]:
                mapping[word] = enum

        return mapping

    def translate_word(self, word: str) -> Optional[TrackWorkEnum]:
        direct_correspondence = getattr(TrackWorkEnum, word.upper(), None)
        if direct_correspondence:
            return direct_correspondence
        else:
            return self._word_to_enum_mapping.get(word, None)
