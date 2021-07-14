from loguru import logger

logger = logger.opt(colors=True)

from sr.audio.recording import Recording
from speech_recognition.recorder.AbstractRecorder import AbstractRecorder


class Recorder(AbstractRecorder):
    def listen(self) -> None:
        while True:
            recording = Recording(source=self.source)
            self._wait_for_phrase_start(recording=recording)
            self._wait_for_phrase_end(recording=recording)

            if recording.is_speech:
                self.emit(recording)

    def _wait_for_phrase_start(self, recording: Recording) -> None:
        logger.opt(raw=True, colors=True).warning("<magenta>--------------------------------------- Rec.</>\n")
        while not recording.is_start_valid:
            recording.read()

        recording.frames = recording.frames[-recording.config.start_window_duration:]

    def _wait_for_phrase_end(self, recording: Recording) -> None:
        while not recording.is_end_valid():
            recording.read()
