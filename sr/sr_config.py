from os.path import dirname, realpath

root = dirname(realpath(__file__))


class SRConfig:
    TEST_DATA_DIRECTORY = f"{root}/tests/data"
    TEST_DEBUG_DATA_DIRECTORY = f"{root}/tests/debug_data"
    TRAINING_SYNONYMS_DIRECTORY = f"{root}/training/synonyms"
    TRAINING_AUDIO_DIRECTORY = f"{root}/training/audio"
    SYNONYMS_PATH = f"{root}/dictionary/synonyms.py"
    KALDI_VOCABULARY_PATH = f"{root}/grammar/vocabulary.txt"
