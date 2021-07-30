import array
from typing import Optional

import numpy as np
import scipy.fftpack as scp
from loguru import logger
from pydub import AudioSegment

from sr.audio.recording_config import RecordingConfig
from sr.audio.source.audio_source_interface import AudioSourceInterface, make_audio_segment_from_audio_source_buffer

logger = logger.opt(colors=True)


class Recording:
    def __init__(self, source: AudioSourceInterface):
        self._source = source
        self._config = RecordingConfig(source=source)
        self._audio: AudioSegment = make_audio_segment_from_audio_source_buffer(source=source, buffer=b"")

    def to_dict(self):
        return [
            f"duration: {self._audio.duration_seconds:.3f}",
            f"dBFS: {self._audio.dBFS:.1f}",
            f"start dbFS: {self.start_window.dBFS:.1f}",
            f"end dbFS: {self.end_window.dBFS:.1f}",
            f"freq maximum: {self.maximum_voice_frequency:.1f}",
            f"freq maximum energy: {self.maximum_voice_frequency_energy:.1f}",
        ]

    @property
    def samples(self) -> array.array:
        return self._audio.get_array_of_samples()

    @property
    def raw_data(self) -> bytes:
        return self._audio.raw_data()

    @property
    def spectrogram(self):
        from scipy import signal

        return signal.spectrogram(self.samples, self._source.sample_rate)

    def export(self, filename: str) -> None:
        assert filename.endswith(".wav")
        self._audio.export(filename, format="wav")

    @property
    def start_window(self) -> Optional[AudioSegment]:
        if self._audio.duration_seconds < self._config.start_window_duration / 1000:
            return None
        return self._audio[: self._config.start_window_duration]

    @property
    def end_window(self) -> Optional[AudioSegment]:
        if self._audio.duration_seconds < self._config.start_window_duration / 1000:
            return None
        return self._audio[-self._config.start_window_duration:]

    @property
    def is_start_valid(self) -> bool:
        if not self.start_window:
            return False

        self._audio = self._audio[-self._config.start_window_duration:]  # move the start point
        return self.start_window.dBFS >= self._config.minimum_dbfs

    def is_end_valid(self) -> bool:
        return self.end_window.dBFS < self._config.minimum_dbfs

    @property
    def is_speech(self) -> bool:
        if not self._config.minimum_duration < self._audio.duration_seconds < self._config.maximum_duration:
            logger.info(
                f"<yellow>Phrase duration not in the configured boundaries (lasted {self._audio.duration_seconds}s)</>"
            )
            return False

        self._generate_frequency_information()
        if self.maximum_voice_frequency_energy < self._config.minimum_frequency_energy:
            logger.info(
                f"<yellow>Didn't identify a voice, max voice frequency energy : {self.maximum_voice_frequency_energy}</>"
            )
            return False

        return True

    def read(self):
        self._audio += self._source.read()

    def _generate_frequency_information(self):
        # then normalize and convert to numpy array:
        x = np.double(list(self.samples)) / (2 ** 15)

        X = np.abs(scp.fft(x))[0: int(len(x) / 2)]
        freq_window_start, freq_window_end = 50, 400
        voice_frequencies = list(X[freq_window_start:freq_window_end])
        self.maximum_voice_frequency_energy = max(voice_frequencies)
        self.maximum_voice_frequency = voice_frequencies.index(self.maximum_voice_frequency_energy) + freq_window_start
