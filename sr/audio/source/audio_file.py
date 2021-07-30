from pydub import AudioSegment

from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.errors.end_of_stream_error import EndOfStreamError


class AudioFile(AudioSourceInterface):
    def __init__(self, path: str):
        self.name = path
        self.sound = AudioSegment.from_wav(path)
        self.samples = self.sound.get_array_of_samples()
        self.duration = self.sound.duration_seconds * 1000
        self.sample_rate = self.sound.frame_rate
        self.sample_width = self.sound.sample_width
        self.chunk_size = int(0.001 * self.sample_rate * self.WINDOW_MS)
        self._current_position_ms = 0

    def read(self) -> AudioSegment:
        if self.duration == self._current_position_ms:
            raise EndOfStreamError()
        end_window_ms = min(self._current_position_ms + self.WINDOW_MS, self.duration)
        segment = self.sound[self._current_position_ms: end_window_ms]
        self._current_position_ms = end_window_ms
        return segment
