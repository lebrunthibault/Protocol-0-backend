import subprocess
import threading
from typing import Optional

from loguru import logger

from lib.observable import Observable
from server.p0_script_api_client import p0_script_api_client
from sr.audio.recorder import Recorder
from sr.audio.recording import Recording
from sr.audio.source.abstract_audio_source import AbstractAudioSource
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.errors.end_of_stream_error import EndOfStreamError
from sr.recognizer.recognizer import Recognizer

logger = logger.opt(colors=True)


class AbstractSpeechRecognition(Observable):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    SEND_SEARCH_TO_ABLETON = False
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
        self.recorder.subscribe(Recording, self.recognizer.process_recording)
        if self.DEBUG:
            from sr.display.audio_plot import AudioPlot
            self.recorder.subscribe(Recording, AudioPlot.plot_recording)

        # Recognizer listeners
        self.recognizer.subscribe(AbstractRecognizerNotFoundError, self._handle_recognizer_error)
        if self.SEND_SEARCH_TO_ABLETON:
            self.recognizer.subscribe(str, p0_script_api_client.search_track)

    @logger.catch
    def recognize(self):
        self._setup_observers()

        if self.USE_GUI:
            from sr.display.speech_gui import SpeechGui  # faster bootstrapping
            gui = SpeechGui()
            self.recognizer.subscribe(str, gui.process_message)
            self.subscribe(str, gui.process_message)
            threading.Thread(target=gui.create_window, daemon=True).start()

        try:
            self.recorder.listen()
        except EndOfStreamError:
            return

    def _handle_recognizer_error(self, error: AbstractRecognizerNotFoundError):
        logger.warning(error.DESCRIPTION)
        self.emit(error.LABEL)

        if self.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            subprocess.Popen(
                [
                    "python",
                    "C:\\Users\\thiba\\Google Drive\\music\\dev\\protocol0_system\\scripts\\cli.py",
                    "search_set_gui",
                ],
                shell=True,
                stdin=None,
                stdout=None,
                stderr=None,
                close_fds=True,
            )
