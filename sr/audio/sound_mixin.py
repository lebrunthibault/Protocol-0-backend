import array

from loguru import logger
from pydub import AudioSegment
from typing_extensions import Protocol

from sr.audio.recording_config import RecordingConfig

logger = logger.opt(colors=True)


class SoundMixin(Protocol):
    audio: AudioSegment
    
    def to_dict(self):
        return [
            f"duration: {self.duration_seconds:.3f}s",
            f"dBFS: {self.audio.dBFS:.1f}",
            f"start dbFS: {self._start_window.dBFS:.1f}",
            f"end dbFS: {self._end_window.dBFS:.1f}",
        ]

    def __repr__(self):
        return f"{self.__class__.__name__} {{duration: {self.duration_seconds}s, dBFS: {self.audio.dBFS:.2f}}}"

    def export(self, filename: str) -> None:
        assert filename.endswith(".wav")
        self.audio.export(filename, format="wav")

    @property
    def duration_seconds(self) -> array.array:
        return self.audio.duration_seconds

    @property
    def samples(self) -> array.array:
        return self.audio.get_array_of_samples()

    @property
    def raw_data(self) -> bytes:
        return self.audio.raw_data

    @property
    def _start_window(self) -> AudioSegment:
        return self.audio[: RecordingConfig.WINDOW_MS]

    @property
    def _end_window(self) -> AudioSegment:
        return self.audio[-RecordingConfig.WINDOW_MS:]
