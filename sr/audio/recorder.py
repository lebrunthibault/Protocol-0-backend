from loguru import logger

from lib.observable import Observable
from sr.audio.recording import Recording
from sr.audio.source.abstract_audio_source import AbstractAudioSource
from sr.errors.wait_timeout_error import WaitTimeoutError

logger = logger.opt(colors=True)


class Recorder(Observable):
    def __init__(self, source: AbstractAudioSource):
        super().__init__()
        self.source = source
        logger.info(f"Recorder initialized with source {self.source}")

    def listen(self) -> None:
        while True:
            recording = Recording(source=self.source)
            try:
                self._wait_for_phrase_start(recording=recording)
            except WaitTimeoutError as e:
                logger.error(e)
                logger.info("Retrying")
                continue
            self._wait_for_phrase_end(recording=recording)

            if recording.is_speech:
                self.emit(recording)

    def _wait_for_phrase_start(self, recording: Recording) -> None:
        logger.opt(raw=True, colors=True).warning("<magenta>--------------------------------------- Rec.</>\n")
        while not recording.is_start_valid:
            recording.read()

    def _wait_for_phrase_end(self, recording: Recording) -> None:
        while not recording.is_end_valid():
            recording.read()
