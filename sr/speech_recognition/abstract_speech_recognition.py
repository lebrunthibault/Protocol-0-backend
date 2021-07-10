import subprocess
from typing import Optional

from loguru import logger

from server.p0_script_api_client import p0_script_api_client
from sr.Recognizer import Recognizer, RecognizerStep
from sr.speech_gui import SpeechGui

logger = logger.opt(colors=True)
from vosk import KaldiRecognizer

from speech_recognition.audio_data.AudioData import AudioData
from speech_recognition.audio_source.Microphone import Microphone
from speech_recognition.recorder.RecorderBackground import RecorderBackground
from speech_recognition.recorder.SimpleRecorder import SimpleRecorder


class AbstractSpeechRecognition():
    AUTO_SWITCH_TO_KEYBOARD_SEARCH = False
    FINAL_PROCESSING_STEP = RecognizerStep.DICTIONARY
    MODEL = "p0"
    REFERENCE_MODEL = "us_small"

    def __init__(self):
        self.gui = SpeechGui()
        self.mic = Microphone()
        self.recorder = SimpleRecorder(source=self.mic)
        self.recorder.energy_threshold = 450
        self.recorder.pause_threshold = 0.1
        self.recorder.phrase_threshold = 0.15
        self.recognizers: List[KaldiRecognizer] = []

        self._init_recognizers()
        assert len(self.recognizers), "You should at least configure one Recognizer"

    def recognize(self):
        self.gui.create_window(self._launch_background_recognition)

    def _init_recognizers(self):
        self.recognizers = [
            Recognizer(model_name=self.MODEL, sample_rate=self.mic.SAMPLE_RATE, use_word_list=True),
            # Recognizer(model_name=self.REFERENCE_MODEL, sample_rate=self.mic.SAMPLE_RATE)
        ]

    def _launch_background_recognition(self) -> None:
        RecorderBackground.listen_in_background(recorder=self.recorder,
                                                callback=self._process_audio_phrase)

    def _process_audio_phrase(self, audio: Optional[AudioData]):
        if not audio:
            self.logger.error("No audio found")
            return
        results = [recognizer.process_audio_phrase(audio=audio) for recognizer in self.recognizers]

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
        self.gui.update_text(word)
        logger.info(f"sending search {word} to api")
        p0_script_api_client.search_track(search=word)

    def _handle_not_found(self, failed_step: RecognizerStep):
        if failed_step == RecognizerStep.RECOGNIZER:
            logger.warning("<red><dim>Kaldi couldn't identify a word</></>")
            self.gui.update_text("Kaldi not found")
        else:
            logger.warning("<red><dim>Word found doesn't belong to dictionary</></>")
            self.gui.update_text("Dictionary not found")

        if self.AUTO_SWITCH_TO_KEYBOARD_SEARCH:
            subprocess.Popen(
                ["python", "C:\\Users\\thiba\\Google Drive\\music\\dev\\Protocol0 System\\scripts\\cli.py",
                 "search_set_gui"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    def _exit(self):
        self.recorder.stop()
        self.gui.exit()
