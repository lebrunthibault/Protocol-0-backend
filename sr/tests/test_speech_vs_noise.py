import glob
import json
import os
import subprocess
from typing import List

import pytest

from lib.utils import filename_datetime
from sr.audio.recording import Recording
from sr.audio.source.audio_file import AudioFile
from sr.speech_recognition.speech_recognition import SpeechRecognition
from sr.sr_config import SRConfig


class SpeechRecognitionTest(object):
    def __init__(self, source: AudioFile):
        self._source = source
        self._recordings: List[Recording] = []
        self._debug_data_directory = os.path.normpath(f"{SRConfig.TEST_DEBUG_DATA_DIRECTORY}/{filename_datetime()}")

        self._sr = SpeechRecognition(source=source)
        self._sr.subscribe(Recording, self._recordings.append)

    def assert_speech(self):
        self._sr.listen()
        assert len(self._recordings) == 1, f"Expected to find one and only one speech recording in {self._source.name}"

    def assert_noise(self):
        self._sr.listen()
        if len(self._recordings) != 0:
            print(f'explorer /select,"{self._debug_data_directory}"')
            os.mkdir(self._debug_data_directory)
            for i, recording in enumerate(self._recordings):
                recording.export(f"{self._debug_data_directory}/recording_{i}.wav")
                with open(f"{self._debug_data_directory}/recording_{i}.json", "w") as f:
                    f.write(json.dumps(recording.to_dict()))
            subprocess.Popen(f'explorer /select,"{self._debug_data_directory}\\recording_0.wav"')

        assert len(self._recordings) == 0, f"In {self._source.name} identified noise as speech"


@pytest.mark.skip
def test_speech_recognition():
    SpeechRecognitionTest(source=AudioFile(f"{SRConfig.TEST_DATA_DIRECTORY}/hello.wav")).assert_speech()
    SpeechRecognitionTest(source=AudioFile(f"{SRConfig.TEST_DATA_DIRECTORY}/noise.wav")).assert_noise()


@pytest.mark.skip
def test_speech_recognition_words():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/words/**/*.wav", recursive=True):
        SpeechRecognitionTest(source=AudioFile(filename)).assert_speech()


@pytest.mark.skip
def test_speech_recognition_noise():
    for filename in glob.glob(f"{SRConfig.TRAINING_AUDIO_DIRECTORY}/noise/**/*.wav", recursive=True):
        SpeechRecognitionTest(source=AudioFile(filename)).assert_noise()
