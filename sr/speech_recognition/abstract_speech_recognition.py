import subprocess
import threading
from abc import abstractmethod

from lib.observable import Observable
from loguru import logger
from sr.audio.recording import Recording
from sr.display.audio_plot import AudioPlot
from sr.display.speech_gui import SpeechGui
from sr.enums.speech_recognition_model_enum import SpeechRecognitionModelEnum
from sr.recognizer.recognizer import Recognizer, RecognizerResult

from speech_recognition.audio_source.AbstractAudioSource import AbstractAudioSource
from speech_recognition.audio_source.Microphone import Microphone
from speech_recognition.errors.AbstractRecognizerNotFoundError import AbstractRecognizerNotFoundError
from speech_recognition.errors.WaitTimeoutError import WaitTimeoutError

logger = logger.opt(colors=True)

from sr.audio.recorder import Recorder


class AbstractSpeechRecognition(Observable):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    USE_GUI = False
    DEBUG = False

    def __init__(self, source: AbstractAudioSource = Microphone()):
        super().__init__()
        self.recorder = Recorder(source=source)
        self.recognizer = Recognizer(
            model=SpeechRecognitionModelEnum.MAIN_MODEL, sample_rate=self.recorder.source.SAMPLE_RATE
        )

    def _setup_observers(self):
        self.recorder.subscribe(Recording, self.recognizer.process_recording)
        if self.DEBUG:
            self.recorder.subscribe(Recording, AudioPlot.plot_recording)

        self.recognizer.subscribe(AbstractRecognizerNotFoundError, self._handle_recognizer_error)
        self.recognizer.subscribe(RecognizerResult, self._process_recognizer_result)

    @logger.catch
    def recognize(self):
        self._setup_observers()

        if self.USE_GUI:
            gui = SpeechGui()
            self.subscribe(object, gui.process_message)
            threading.Thread(target=gui.create_window, daemon=True).start()

        while True:
            try:
                self.recorder.listen()
            except WaitTimeoutError as e:
                logger.error(e)
                logger.info("Retrying")

    @abstractmethod
    def _process_recognizer_result(self, recognizer_result: RecognizerResult):
        raise NotImplementedError

    def _handle_recognizer_error(self, error: AbstractRecognizerNotFoundError):
        logger.warning(error.DESCRIPTION)
        self.emit(error.LABEL)

        if self.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            subprocess.Popen(
                [
                    "python",
                    "C:\\Users\\thiba\\Google Drive\\music\\dev\\Protocol0 System\\scripts\\cli.py",
                    "search_set_gui",
                ],
                shell=True,
                stdin=None,
                stdout=None,
                stderr=None,
                close_fds=True,
            )
