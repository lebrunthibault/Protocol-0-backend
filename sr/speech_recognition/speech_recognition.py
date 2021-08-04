from typing import Optional

from lib.observable import Observable
from loguru import logger
from sr.audio.recorder import get_speech_recordings_observable
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.display.audio_plot import AudioPlot
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.recognizer.null_recognizer import NullRecognizer
from sr.recognizer.recognizer_interface import RecognizerInterface

logger = logger.opt(colors=True)


class SpeechRecognition(Observable):
    USE_GUI = False
    DEBUG = True

    def __init__(self, source: Optional[AudioSourceInterface] = None, recognizer: Optional[RecognizerInterface] = None):
        super(SpeechRecognition, self).__init__()
        if not source:
            from sr.audio.source.microphone import Microphone

            source = Microphone()
        self._recognizer = recognizer or NullRecognizer()
        self._recognizer.load_model(sample_rate=source.sample_rate)

        speech_stream = get_speech_recordings_observable(source=source)

        # speech_stream.subscribe(self._recognizer.handle_recording, logger.exception)
        # self._recorder.subscribe(Recording, self.emit)

        if self.USE_GUI:
            from sr.display.speech_gui import SpeechGui  # for performance

            gui = SpeechGui()
            self._recognizer.subscribe(str, gui.handle_string_message)
            self._recognizer.subscribe(AbstractRecognizerNotFoundError, gui.handle_string_message)

        speech_stream.subscribe(print, logger.exception)

        if self.DEBUG:
            speech_stream.subscribe(AudioPlot.plot_recording, logger.exception)

    @property
    def recognizer(self) -> RecognizerInterface:
        return self._recognizer
