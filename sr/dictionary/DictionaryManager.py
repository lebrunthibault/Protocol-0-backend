import json
import os
import subprocess

import pystache
from lib.consts import PROJECT_ROOT
from lib.utils import flatten
from loguru import logger
from sr.dictionary.TrackWordEnum import TrackWorkEnum
from sr.dictionary.synonyms import speech_recognition_dictionary


class DictionaryManager():
    RESULT_DIRECTORY = f"{PROJECT_ROOT}/sr/training/words"
    DICTIONARY_PATH = f"{PROJECT_ROOT}/sr/dictionary/synonyms.py"
    KALDI_WORDS_PATH = f"{PROJECT_ROOT}/sr/grammar/vocabulary.txt"

    def __init__(self):
        self.word_synonyms = []

        self.synonyms_set = set()

    def prepare_model_grammar(self):
        with open(self.KALDI_WORDS_PATH, "w") as f:
            f.write(" ".join([enum.name.lower() for enum in TrackWorkEnum]))

        subprocess.run(
            ["bash", "-c",
             "source /home/thibault/.zshrc && cd '/mnt/c/Users/thiba/Google Drive/music/dev/Protocol0 System/sr/grammar' && make prepare"])

        logger.info("grammar generated")

    def generate_from_results(self):
        for word_folder in os.scandir(self.RESULT_DIRECTORY):
            self._generate_from_word_results(word_folder=word_folder)

        logger.info(f"synonyms: {self.word_synonyms}")
        self._write_dictionary_to_file(self.word_synonyms)

    @staticmethod
    def get_word_list():
        track_enum_words = [enum.name.lower() for enum in TrackWorkEnum]
        return ["[unk]", "exit"] + track_enum_words + flatten(speech_recognition_dictionary.values())

    def _generate_from_word_results(self, word_folder):
        word: str = word_folder.name
        logger.info(f"processing word {word}")

        word_enum: TrackWorkEnum = getattr(TrackWorkEnum, word.upper(), None)
        if not word_enum:
            raise NameError(f"The word {word} does not exists in the word enum")

        synonyms = set()

        for entry in os.scandir(word_folder.path):
            with open(entry.path, "r") as f:
                result: dict = json.loads(f.read())['result']
                synonyms.update(result.keys())

        unique_words = list(self.keep_unique_words(list(synonyms)))
        self.synonyms_set.update(synonyms)

        self.word_synonyms.append({"enum_name": word_enum.name, "synonyms": unique_words})

    def keep_unique_words(self, words: list):
        """ keep only words that are not in other word lists
        and remove duplicates from other lists as well
        Each list is composed of unique words that didn't appear in other lists
        """
        for word in words:
            if word not in self.synonyms_set:
                yield word
            else:
                logger.info(f"found duplicate {word}")

                # found a duplicate
                for word_synonyms in self.word_synonyms:
                    if word in word_synonyms["synonyms"]:
                        word_synonyms["synonyms"].remove(word)

    def _write_dictionary_to_file(self, synonyms: list):
        with open(f"{self.DICTIONARY_PATH.replace('py', 'mustache')}", "r") as f:
            mustache_template = f.read()

        code = pystache.render(mustache_template, {"dictionary": synonyms})
        with open(self.DICTIONARY_PATH, "w") as f:
            f.write(code)

        logger.success("Dictionary code written successfully")
        logger.info(self.get_word_list())
