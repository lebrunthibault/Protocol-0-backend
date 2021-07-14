import time
from typing import Optional, List

import numpy as np
import scipy.fftpack as scp
from loguru import logger

logger = logger.opt(colors=True)
from pydub import AudioSegment

from speech_recognition.audio_source.AbstractAudioSource import AbstractAudioSource
from speech_recognition.errors.EndOfStreamError import EndOfStreamError
from speech_recognition.errors.WaitTimeoutError import WaitTimeoutError
from sr.audio.recording_config import RecordingConfig


class Recording:
    def __init__(self, source: AbstractAudioSource):
        self.source = source
        self.config = RecordingConfig(source=source)
        self.frames: List[AudioSegment] = []
        self.audio: AudioSegment = self._make_audio_segment_from_buffer(buffer=b"")
        self.start_at = time.time()

    @property
    def end_at(self) -> float:
        return self.start_at + self.audio.duration_seconds

    @property
    def start_window(self) -> Optional[AudioSegment]:
        if self.audio.duration_seconds < self.config.start_window_duration:
            return None
        return self.audio[: self.config.start_window_duration * 1000]

    @property
    def end_window(self) -> Optional[AudioSegment]:
        if self.audio.duration_seconds < self.config.start_window_duration:
            return None
        return self.audio[-self.config.start_window_duration * 1000 :]

    @property
    def is_start_valid(self) -> bool:
        if not self.start_window:
            return False

        if self.config.maximum_duration and time.time() - self.start_at > self.config.maximum_duration:
            raise WaitTimeoutError("listening timed out while waiting for phrase to start")

        return self.start_window.dBFS >= self.config.minimum_dbfs

    def is_end_valid(self) -> bool:
        return self.end_window.dBFS < self.config.minimum_dbfs

    @property
    def is_speech(self) -> bool:
        if self.audio.duration_seconds < self.config.minimum_duration:
            logger.info("<yellow>Phrase is not long enough, retrying</>")
            return False

        self._generate_frequency_information()
        if self.maximum_voice_frequency_energy < self.config.minimum_frequency_energy:
            logger.info(
                f"<yellow>Didn't identify a voice, max voice frequency energy : {self.maximum_voice_frequency_energy}</>"
            )
            return False

        return True

    def read(self):
        buffer = self.source.read()
        if len(buffer) == 0:
            raise EndOfStreamError
        self.audio += self._make_audio_segment_from_buffer(data=buffer)

    def _generate_frequency_information(self):
        # then normalize and convert to numpy array:
        x = np.double(list(self.audio.get_array_of_samples())) / (2 ** 15)

        X = np.abs(scp.fft(x))[0 : int(len(x) / 2)]
        freq_window_start, freq_window_end = 50, 400
        voice_frequencies = list(X[freq_window_start:freq_window_end])
        self.maximum_voice_frequency_energy = max(voice_frequencies)
        self.maximum_voice_frequency = voice_frequencies.index(self.maximum_voice_frequency_energy) + freq_window_start

    def _make_audio_segment_from_buffer(self, buffer: bytes) -> AudioSegment:
        return AudioSegment(
            data=buffer, sample_width=self.source.SAMPLE_WIDTH, frame_rate=self.source.SAMPLE_RATE, channels=1
        )
