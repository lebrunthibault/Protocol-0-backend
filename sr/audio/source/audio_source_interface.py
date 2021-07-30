from typing import Any

from pydub import AudioSegment
from typing_extensions import Protocol


class AudioSourceInterface(Protocol):
    WINDOW_MS = 20

    name: str
    stream: Any
    sample_rate: int
    sample_width: int

    @property
    def window_size(self):
        return int(0.001 * self.sample_rate * self.WINDOW_MS)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.sample_rate} Hz, {self.sample_width * 8} bits, window: {self.window_size} samples, {self.WINDOW_MS} ms"

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self):
        raise NotImplementedError()

    def read(self) -> AudioSegment:
        raise NotImplementedError()


def make_audio_segment_from_audio_source_buffer(source: AudioSourceInterface, buffer: bytes):
    return AudioSegment(data=buffer, sample_width=source.sample_width, frame_rate=source.sample_rate, channels=1)
