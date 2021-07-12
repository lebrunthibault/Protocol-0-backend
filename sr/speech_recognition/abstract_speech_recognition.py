import subprocess
import threading

from lib.observable import Observable, Event
from loguru import logger
from server.p0_script_api_client import p0_script_api_client
from sr.display.audio_plot import AudioPlot
from sr.display.speech_gui import SpeechGui
from sr.recognizer.Recognizer import Recognizer, RecognizerStep
from sr.training.audio_export import AudioExport

from speech_recognition.audio_data.Recording import Recording
from speech_recognition.errors.WaitTimeoutError import WaitTimeoutError

logger = logger.opt(colors=True)
from vosk import KaldiRecognizer

from speech_recognition.audio_source.Microphone import Microphone
from speech_recognition.recorder.SimpleRecorder import SimpleRecorder


class AbstractSpeechRecognition(Observable):
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    USE_GUI = False
    DEBUG = False
    SEND_SEARCH_TO_ABLETON = False
    FINAL_PROCESSING_STEP = RecognizerStep.DICTIONARY
    MODEL = "p0"
    REFERENCE_MODEL = "us_small"

    def __init__(self):
        super().__init__()
        self.mic = Microphone()
        logger.info("Mic initialized")
        self.recorder = SimpleRecorder(source=self.mic)
        self.recorder.subscribe(self._process_recording)
        if self.DEBUG:
            self.recorder.subscribe(AudioPlot.receive_recorder_event)
        self.recorder.subscribe(AudioExport.receive_recorder_event)
        self.recognizers: List[KaldiRecognizer] = []

        self._init_recognizers()
        assert len(self.recognizers), "You should at least configure one Recognizer"

    def recognize(self):
        if self.USE_GUI:
            gui = SpeechGui()
            self.subscribe(gui.receive_event)
            threading.Thread(target=gui.create_window, daemon=True).start()

        self._launch_recognition()

    def _init_recognizers(self):
        self.recognizers = [
            Recognizer(model_name=self.MODEL, sample_rate=self.mic.SAMPLE_RATE, use_word_list=True),
        ]

    @logger.catch
    def _launch_recognition(self) -> None:
        while True:
            try:
                self.recorder.listen()
            except WaitTimeoutError as e:
                logger.error(e)
                logger.info("Retrying")

    def _process_recording(self, event: Event):
        if not isinstance(event.data, Recording):
            return
        logger.info("processing recording")
        results = [recognizer.process_recording(recording=event.data) for recognizer in
                   self.recognizers]

        if all(result.raw_result is None for result in results):
            self._handle_not_found(failed_step=RecognizerStep.RECOGNIZER)
            return

        if self.FINAL_PROCESSING_STEP == RecognizerStep.RECOGNIZER:
            self._handle_success(results[0])
            return

        # FINAL_PROCESSING_STEP is RecognizerStep.DICTIONARY
        word_enums = list(filter(None, set([result.word_enum for result in results])))
        if len(word_enums) != 1:
            if len(word_enums) > 1:
                logger.error(f"dictionary mismatch, found multiple word enums: {word_enums}")
            self._handle_not_found(failed_step=RecognizerStep.DICTIONARY)
            return

        self._handle_success(word_enums[0].name)

    def _handle_success(self, word: str):
        logger.success(f"Found word enum: {word}")
        self.emit(word)
        if self.SEND_SEARCH_TO_ABLETON:
            logger.info(f"sending search {word} to api")
            p0_script_api_client.search_track(search=word)

    def _handle_not_found(self, failed_step: RecognizerStep):
        if failed_step == RecognizerStep.RECOGNIZER:
            logger.warning("<red><dim>Kaldi couldn't identify a word</></>")
            self.emit("Kaldi not found")
        else:
            logger.warning("<red><dim>Word found doesn't belong to dictionary</></>")
            self.emit("Dictionary not found")

        if self.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            subprocess.Popen(
                ["python", "C:\\Users\\thiba\\Google Drive\\music\\dev\\Protocol0 System\\scripts\\cli.py",
                 "search_set_gui"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
