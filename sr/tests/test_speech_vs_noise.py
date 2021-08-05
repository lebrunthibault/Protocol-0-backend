import glob
import json
import os
import subprocess
from functools import partial
from shutil import rmtree
from typing import List, Callable

import pytest
from loguru import logger

from sr.audio.short_sound import SoundMixin
from sr.audio.source.audio_file import AudioFile
from sr.audio.speech_sound import SpeechSound, get_speech_sounds_observable
from sr.sr_config import SRConfig


def debug_sounds(speech_sounds: List[SoundMixin]):
    rmtree(SRConfig.TEST_DEBUG_DATA_DIRECTORY)
    os.mkdir(SRConfig.TEST_DEBUG_DATA_DIRECTORY)
    for i, speech_sound in enumerate(speech_sounds):
        print(speech_sound.to_dict())
        speech_sound.export(f"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\speech_sound_{i}.wav")
        with open(f"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\speech_sound_{i}.json", "w") as f:
            f.write(json.dumps(speech_sound.to_dict()))

    subprocess.Popen(f'explorer /select,"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\speech_sound_0.wav"')


def _test_audio_file(filename: str, assert_callable: Callable):
    speech_sounds = []
    source = AudioFile(filename if os.path.isabs(filename) else f"{SRConfig.TEST_DATA_DIRECTORY}\\{filename}")

    def on_complete():
        try:
            assert_callable(speech_sounds=speech_sounds)
        except AssertionError as e:
            debug_sounds(speech_sounds=speech_sounds)
            raise e

        # debug_speech_sounds(speech_sounds=speech_sounds)

    get_speech_sounds_observable(source=source).subscribe(speech_sounds.append, logger.exception, on_complete)


def assert_speech(speech_sounds: List[SpeechSound], speech_count=1):
    assert len(
        speech_sounds) == speech_count, f"Expected to find {speech_count} speech speech_sound(s), got {len(speech_sounds)}"


def assert_noise(speech_sounds: List[SpeechSound]):
    assert len(speech_sounds) == 0, f"identified noise as speech"


# @pytest.mark.skip
def test_speech_recognition():
    _test_audio_file("hello.wav", partial(assert_speech, speech_count=1))
    _test_audio_file("hello_multiple.wav", partial(assert_speech, speech_count=3))
    _test_audio_file("noise.wav", assert_noise)


@pytest.mark.skip
def test_speech_recognition_words():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/words/**/*.wav", recursive=True):
        _test_audio_file(filename, partial(assert_speech, speech_count=1))


@pytest.mark.skip(reason="Recognizer not good enough atm")
def test_speech_recognition_noise():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/noise/**/*.wav", recursive=True):
        _test_audio_file(filename, partial(assert_noise))
