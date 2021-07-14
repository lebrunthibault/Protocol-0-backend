from lib.consts import PROJECT_ROOT


class Config:
    TEST_DATA_DIRECTORY = f"{PROJECT_ROOT}/sr/tests/data"
    TRAINING_SYNONYMS_DIRECTORY = f"{PROJECT_ROOT}/sr/training/synonyms"
    TRAINING_AUDIO_DIRECTORY = f"{PROJECT_ROOT}/sr/training/audio"
    SYNONYMS_PATH = f"{PROJECT_ROOT}/sr/dictionary/synonyms.py"
    KALDI_VOCABULARY_PATH = f"{PROJECT_ROOT}/sr/grammar/vocabulary.txt"
