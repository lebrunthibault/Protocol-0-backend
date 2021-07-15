from pydub import AudioSegment

from sr.audio.source.abstract_audio_source import AbstractAudioSource
from sr.errors.end_of_stream_error import EndOfStreamError


class AudioFile(AbstractAudioSource):
    def __init__(self, path: str):
        self.sound = AudioSegment.from_wav(path)
        self.samples = self.sound.get_array_of_samples()
        self.duration = self.sound.duration_seconds * 1000
        # self.window_size = int(0.001 * sample_rate * self.WINDOW_MS)
        # self.step_size = int(0.001 * sample_rate * self.STEP_MS)
        self.sample_rate = self.sound.frame_rate
        self.sample_width = self.sound.sample_width
        self.chunk_size = int(0.001 * self.sample_rate * self.WINDOW_MS)
        self._current_position_ms = 0

    def read(self) -> AudioSegment:
        end_window_ms = self._current_position_ms + self.WINDOW_MS
        if self.duration < end_window_ms:
            raise EndOfStreamError()
        segment = self.sound[self._current_position_ms:end_window_ms]
        self._current_position_ms += self.WINDOW_MS
        return segment
