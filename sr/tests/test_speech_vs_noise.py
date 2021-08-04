import asyncio
import glob
import json
import os
import subprocess
from functools import partial
from shutil import rmtree
from typing import List, Callable

import pytest
from loguru import logger

from sr.audio.recorder import get_speech_recordings_observable
from sr.audio.short_sound import ShortSound
from sr.audio.source.audio_file import AudioFile
from sr.sr_config import SRConfig


def debug_recordings(recordings: List[ShortSound]):
    rmtree(SRConfig.TEST_DEBUG_DATA_DIRECTORY)
    os.mkdir(SRConfig.TEST_DEBUG_DATA_DIRECTORY)
    for i, recording in enumerate(recordings):
        print(recording.to_dict())
        recording.export(f"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\recording_{i}.wav")
        with open(f"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\recording_{i}.json", "w") as f:
            f.write(json.dumps(recording.to_dict()))

    subprocess.Popen(f'explorer /select,"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}\\recording_0.wav"')


def _test_audio_file(filename: str, assert_callable: Callable):
    recordings = []
    source = AudioFile(filename if os.path.isabs(filename) else f"{SRConfig.TEST_DATA_DIRECTORY}\\{filename}")

    def on_complete():
        try:
            assert_callable(recordings=recordings)
        except AssertionError as e:
            debug_recordings(recordings=recordings)
            raise e

        # debug_recordings(recordings=recordings)

    get_speech_recordings_observable(source=source).subscribe(recordings.append, logger.exception, on_complete)


def assert_speech(recordings: List[ShortSound], speech_count=1):
    assert len(
        recordings) == speech_count, f"Expected to find {speech_count} speech recording(s), got {len(recordings)}"


def assert_noise(recordings: List[ShortSound]):
    assert len(recordings) == 0, f"identified noise as speech"


@pytest.mark.skip
def test_speech_recognition():
    # _test_audio_file("hello.wav", partial(assert_speech, speech_count=1))
    _test_audio_file("hello_multiple.wav", partial(assert_speech, speech_count=3))
    # _test_audio_file("noise.wav", assert_noise)


def test_asyncio():
    loop = asyncio.get_event_loop()
    print("forever")
    loop.run_forever()
    print("done")
    # future = asyncio.Future()
    # await future
    # print("done")
    # return
    # loop = asyncio.get_event_loop()
    # loop.run_forever()
    # await toto()


#
#
# async def toto():
#     await wait()
#     print("closing stuff")
#
#
# async def wait():
#     print("doing async stuff")
#     await asyncio.sleep(1)
#     print("finished async stuff")


@pytest.mark.skip
def test_speech_recognition_words():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/words/**/*.wav", recursive=True):
        _test_audio_file(filename, partial(assert_speech, speech_count=1))


@pytest.mark.skip(reason="Recognizer not good enough atm")
def test_speech_recognition_noise():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/noise/**/*.wav", recursive=True):
        _test_audio_file(filename, partial(assert_noise))
