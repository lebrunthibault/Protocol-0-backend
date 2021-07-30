import os
from functools import partial
from os.path import exists

from lib.utils import filename_datetime
from sr.audio.recording import Recording
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.recognizer.recognizer import Recognizer
from sr.speech_recognition.speech_recognition import SpeechRecognition
from sr.sr_config import SRConfig


class SpeechRecognitionTrainingSetCollector(object):
    @classmethod
    def collect(cls, target_word: str):
        assert (
            target_word == "noise" or target_word in AbletonCommandEnum.words()
        ), "word should be 'noise' or in the word enum"
        sr = SpeechRecognition(recognizer=Recognizer())
        sr.recognizer.subscribe(Recording, partial(cls._export_recognizer_result, target_word=target_word))
        sr.listen()

    @classmethod
    def _export_recognizer_result(cls, target_word: str, recording: Recording):
        """ Export recording to appropriate directory for training """
        sample_subdir = "noise" if target_word == "noise" else f"words/{target_word}"
        sample_directory = f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/{sample_subdir}"
        if not exists(sample_directory):
            os.mkdir(sample_directory)

        recording.export(f"{sample_directory}/{filename_datetime()}.wav")
