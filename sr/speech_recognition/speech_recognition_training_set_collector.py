import os
from functools import partial
from os.path import exists

from loguru import logger

from lib.utils import filename_datetime
from sr.audio.recorder import get_short_sounds_observable
from sr.audio.short_sound import ShortSound
from sr.audio.source.microphone import Microphone
from sr.enums.ableton_command_enum import AbletonCommandEnum
from sr.rx.rx_utils import rx_error
from sr.sr_config import SRConfig


def collect_short_sound_recordings(target_word: str):
    assert (
        target_word == "noise" or target_word in AbletonCommandEnum.words()
    ), "word should be 'noise' or in the word enum"
    get_short_sounds_observable(source=Microphone()).subscribe(
        partial(_export_recognizer_result, target_word=target_word), rx_error)


def _export_recognizer_result(short_sound: ShortSound, target_word: str):
    """ Export recording to appropriate directory for training """
    logger.info(f"saving {repr(short_sound)} as {target_word}")
    sample_subdir = "noise" if target_word == "noise" else f"words/{target_word}"
    sample_directory = f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/{sample_subdir}"
    if not exists(sample_directory):
        os.mkdir(sample_directory)

    short_sound.export(f"{sample_directory}/{filename_datetime()}.wav")
