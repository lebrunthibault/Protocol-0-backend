from typing import Optional

from loguru import logger

from lib.observable import Observable
from sr.audio.recorder import Recorder
from sr.audio.recording import Recording
from sr.audio.source.audio_source_interface import AudioSourceInterface
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.recognizer.null_recognizer import NullRecognizer
from sr.recognizer.recognizer_interface import RecognizerInterface

logger = logger.opt(colors=True)


class SpeechRecognition(Observable):
    USE_GUI = False
    DEBUG = False

    def __init__(self, source: Optional[AudioSourceInterface] = None, recognizer: Optional[RecognizerInterface] = None):
        super(SpeechRecognition, self).__init__()
        #
        # # transitions
        # # transitions = [
        # #     ["start", SpeechRecognitionStateEnum.UN_STARTED, SpeechRecognitionStateEnum.STARTED],
        # #     ["terminate", SpeechRecognitionStateEnum.STARTED, SpeechRecognitionStateEnum.TERMINATED],
        # #     ["error", SpeechRecognitionStateEnum.STARTED, SpeechRecognitionStateEnum.ERRORED],
        # # ]
        # transitions = [
        #     SpeechRecognitionStateEnum.LISTEN.value, SpeechRecognitionStateEnum.INIT, SpeechRecognitionStateEnum.LISTEN,
        #     SpeechRecognitionStateEnum.RECOGNIZE.value, SpeechRecognitionStateEnum.LISTEN, SpeechRecognitionStateEnum.RECOGNIZE,
        #     SpeechRecognitionStateEnum.TRANSLATE.value, SpeechRecognitionStateEnum.RECOGNIZE, SpeechRecognitionStateEnum.TRANSLATE,
        # ]
        #
        # states = [
        #     State(SpeechRecognitionStateEnum.INIT),
        #     State(SpeechRecognitionStateEnum.LISTEN, on_enter=[self.recognize]),
        #     State(SpeechRecognitionStateEnum.ANALYZE, on_enter=[self._on_terminate]),
        # ]
        #
        # self._state_machine = Machine(states=states, transitions=transitions, initial=SpeechRecognitionStateEnum.UN_STARTED)
        #
        # self.machine = Machine(model=self, states=list(SpeechRecognitionStateEnum), initial=SpeechRecognitionStateEnum.INIT)

        if not source:
            from sr.audio.source.microphone import Microphone

            source = Microphone()
        self._recorder = Recorder(source=source)
        self._recognizer = recognizer or NullRecognizer()
        self._recognizer.load_model(sample_rate=source.sample_rate)

        self._recorder.subscribe(Recording, self._recognizer.handle_recording)

        if self.USE_GUI:
            from sr.display.speech_gui import SpeechGui  # for performance

            gui = SpeechGui()
            self._recognizer.subscribe(str, gui.handle_string_message)
            self._recognizer.subscribe(AbstractRecognizerNotFoundError, gui.handle_string_message)

        if self.DEBUG:
            from sr.display.audio_plot import AudioPlot

            self._recorder.subscribe(Recording, AudioPlot.plot_recording)
            self._recorder.subscribe(Recording, self.emit)

    @property
    def recognizer(self) -> RecognizerInterface:
        return self._recognizer

    def listen(self):
        self._recorder.listen()
