import json
import os
import subprocess
from typing import List, Set

import pystache
from lib.utils import flatten
from loguru import logger
from sr.dictionary.synonyms import speech_recognition_dictionary
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


class DictionaryManager:
    def __init__(self):
        self.word_synonyms = []
        self.synonyms_set: Set[str] = set()

    def prepare_model_grammar(self) -> None:
        with open(SRConfig.KALDI_VOCABULARY_PATH, "w") as f:
            f.write(" ".join(AbletonCommandEnum.words()))

        subprocess.run(
            [
                "bash",
                "-c",
                "source /home/thibault/.zshrc && cd '/mnt/c/Users/thiba/Google Drive/music/dev/protocol0_system/sr/grammar' && make prepare",
            ]
        )

        logger.info("grammar generated")

    def generate_from_results(self) -> None:
        for word_folder in os.scandir(SRConfig.TRAINING_SYNONYMS_DIRECTORY):
            # noinspection PyTypeChecker
            self._generate_from_word_results(word_folder=word_folder)

        logger.info(f"synonyms: {self.word_synonyms}")
        self._write_dictionary_to_file(self.word_synonyms)

    @staticmethod
    def get_word_list() -> List[str]:
        track_enum_words = [enum.name.lower() for enum in AbletonCommandEnum]
        return ["[unk]", "exit"] + track_enum_words + flatten(speech_recognition_dictionary.values())

    def _generate_from_word_results(self, word_folder) -> None:
        word: str = word_folder.name
        logger.info(f"processing word {word}")

        word_enum: AbletonCommandEnum = getattr(AbletonCommandEnum, word.upper(), None)
        if not word_enum:
            raise NameError(f"The word {word} does not exists in the word enum")

        synonyms = set()

        for entry in os.scandir(word_folder.path):
            # noinspection PyUnresolvedReferences
            with open(entry.path, "r") as f:
                result: dict = json.loads(f.read())["result"]
                synonyms.update(result.keys())

        unique_words = list(self._keep_unique_words(list(synonyms)))
        self.synonyms_set.update(synonyms)

        self.word_synonyms.append({"enum_name": word_enum.name, "synonyms": unique_words})

    def _keep_unique_words(self, words: List[str]):
        """keep only words that are not in other word lists
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
        with open(f"{SRConfig.SYNONYMS_PATH.replace('py', 'mustache')}", "r") as f:
            mustache_template = f.read()

        code = pystache.render(mustache_template, {"dictionary": synonyms})
        with open(SRConfig.SYNONYMS_PATH, "w") as f:
            f.write(code)

        logger.success("Dictionary code written successfully")
        logger.info(self.get_word_list())
