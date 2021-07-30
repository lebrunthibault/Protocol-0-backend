from loguru import logger

from lib.observable import Observable
from sr.audio.recording import Recording
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.errors.end_of_stream_error import EndOfStreamError
from sr.errors.wait_timeout_error import WaitTimeoutError

logger = logger.opt(colors=True)


class Recorder(Observable):
    def __init__(self, source: AudioSourceInterface):
        super().__init__()
        self._source = source
        self.sample_rate = self._source.sample_rate
        logger.info(f"Recorder initialized with source {self._source}")

    @logger.catch
    def listen(self):
        try:
            self._listen()
        except EndOfStreamError:
            return

    def _listen(self) -> None:
        while True:
            recording = Recording(source=self._source)
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
        logger.opt(raw=True, colors=True).debug("<magenta>--------------------------------------- Rec.</>\n")
        while not recording.is_start_valid:
            recording.read()

    def _wait_for_phrase_end(self, recording: Recording) -> None:
        try:
            while not recording.is_end_valid():
                recording.read()
        except EndOfStreamError:
            pass
