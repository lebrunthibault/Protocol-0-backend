from loguru import logger
from rx import operators as op
from sdk_generation.p0_script.api_client.p0_script_api.api.default_api import DefaultApi

from sr.audio.source.microphone import Microphone
from sr.audio.speech_sound import get_speech_sounds_observable
from sr.audio.utils import audio_export_sound, audio_plot_sound
from sr.errors.abstract_recognizer_not_found_error import AbstractRecognizerNotFoundError
from sr.recognizer.recognizer import Recognizer
from sr.recognizer.recognizer_result import RecognizerResult
from sr.rx.rx_utils import rx_error, rx_print

logger = logger.opt(colors=True)

USE_GUI = True
DEBUG = False


def recognize_speech():
    script_api = DefaultApi()
    source = Microphone()
    recognizer = Recognizer()
    recognizer.load_model(sample_rate=source.sample_rate)
    speech_stream = get_speech_sounds_observable(source=source)
    recognizer_result_stream = speech_stream.pipe(op.map(recognizer.process_speech_sound), op.share())  # type: ignore
    recognizer_result_stream.subscribe(rx_print, rx_error)
    recognizer_result_stream.subscribe(lambda res: script_api.execute_command(str(res)))

    if USE_GUI:
        from sr.display.speech_gui import SpeechGui  # for performance

        gui = SpeechGui()
        recognizer_result_stream.pipe(op.filter(lambda v: isinstance(v, RecognizerResult)),
                                      op.map(lambda v: v.word)).subscribe(gui.handle_string_message, logger.exception)
        recognizer_result_stream.pipe(op.filter(lambda v: isinstance(v, AbstractRecognizerNotFoundError))).subscribe(
            gui.handle_string_message, logger.exception)

    if DEBUG:
        speech_stream.subscribe(audio_plot_sound, logger.exception)
        speech_stream.subscribe(audio_export_sound, logger.exception)
