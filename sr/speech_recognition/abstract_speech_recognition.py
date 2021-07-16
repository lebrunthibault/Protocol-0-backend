import threading
from typing import Optional

from loguru import logger

from lib.observable import Observable
from sr.audio.recorder import Recorder
from sr.audio.recording import Recording
from sr.audio.source.abstract_audio_source import AbstractAudioSource
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.errors.end_of_stream_error import EndOfStreamError
from sr.recognizer.recognizer import Recognizer

logger = logger.opt(colors=True)


class AbstractSpeechRecognition(Observable):
    USE_GUI = False
    DEBUG = False

    def __init__(self, source: Optional[AbstractAudioSource] = None, recognizer: Optional[Recognizer] = None):
        super().__init__()
        if not source:
            from sr.audio.source.microphone import Microphone
            source = Microphone()
        self.recorder = Recorder(source=source)
        self.recognizer = recognizer or Recognizer(
            model=SpeechRecognitionModelEnum.MAIN_MODEL, sample_rate=source.sample_rate
        )

    def _setup_observers(self):
        # Recorder listeners
        self.recorder.subscribe(Recording, self.recognizer.handle_recording)
        if self.DEBUG:
            from sr.display.audio_plot import AudioPlot
            self.recorder.subscribe(Recording, AudioPlot.plot_recording)

        # Recognizer listeners
        self.recognizer.subscribe(AbstractRecognizerNotFoundError, self._handle_recognizer_error)

    @logger.catch
    def recognize(self):
        self._setup_observers()

        if self.USE_GUI:
            from sr.display.speech_gui import SpeechGui  # for performance
            gui = SpeechGui()
            self.recognizer.subscribe(str, gui.handle_string_message)
            self.subscribe(str, gui.handle_string_message)
            threading.Thread(target=gui.create_window, daemon=True).start()

        try:
            self.recorder.listen()
        except EndOfStreamError:
            return

    def _handle_recognizer_error(self, error: AbstractRecognizerNotFoundError):
        logger.warning(error.DESCRIPTION)
        self.emit(error.LABEL)
