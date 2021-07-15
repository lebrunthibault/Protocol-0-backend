from pydub import AudioSegment


class AbstractAudioSource(object):
    WINDOW_MS = 20
    STEP_MS = 10

    def __init__(self):
        self.name = None
        self.stream = None
        self.sample_rate = None
        self.sample_width = None
        raise NotImplementedError("this is an abstract class")

    @property
    def window_size(self):
        return int(0.001 * self.sample_rate * self.WINDOW_MS)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.sample_rate} Hz, {self.sample_width * 8} bits, window: {self.window_size} samples, {self.WINDOW_MS} ms"

    def __enter__(self):
        raise NotImplementedError("this is an abstract class")

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError("this is an abstract class")

    def read(self):
        raise NotImplementedError("this is an abstract class")

    def close(self):
        raise NotImplementedError("this is an abstract class")

    def make_audio_segment_from_buffer(self, buffer: bytes):
        # def make_audio_segment_from_buffer(self, buffer: bytes) -> AudioSegment:
        return AudioSegment(
            data=buffer, sample_width=self.sample_width, frame_rate=self.sample_rate, channels=1
        )
