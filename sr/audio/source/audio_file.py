import math

from pydub import AudioSegment
from rx import create, Observable
from rx.disposable import Disposable
from rx.subject import ReplaySubject
from sr.audio.recording_config import RecordingConfig
from sr.audio.source.audio_source_interface import AudioSourceInterface


class AudioFile(AudioSourceInterface):
    def __init__(self, path: str):
        self.name = path
        self._audio = AudioSegment.from_wav(path)
        self.sample_rate = self._audio.frame_rate
        self.sample_width = self._audio.sample_width

    def make_observable(self) -> Observable:
        source_subject = ReplaySubject()  # needed when we read a sync source
        create(self._make_observable).subscribe(source_subject)

        return source_subject

    def _make_observable(self, observer, _) -> Disposable:
        duration_ms = self._audio.duration_seconds * 1000
        for i in range(math.ceil(duration_ms / RecordingConfig.BUFFER_MS)):
            right_boundary = min((i + 1) * RecordingConfig.BUFFER_MS, duration_ms)
            observer.on_next(self._audio[i * RecordingConfig.BUFFER_MS: right_boundary])

        observer.on_completed()
        return Disposable()
