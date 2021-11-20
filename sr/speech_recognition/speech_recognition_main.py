import ctypes

from loguru import logger
from rx import operators as op, Observable

from api.p0_script_api_client import protocol0
from config import SystemConfig
from lib.ableton import is_ableton_focused
from lib.decorators import log_exceptions
from lib.rx import rx_nop
from sr.audio.source.microphone import Microphone
from sr.audio.speech_sound import get_speech_sounds_observable
from sr.enums.speech_command_enum import SpeechCommandEnum
from sr.recognizer.recognizer import Recognizer
from sr.recognizer.recognizer_result import export_recognizer_result
from sr.speech_recognition.speech_command_manager import process_speech_command
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


class StreamProvider:
    def __init__(self):
        source = Microphone()
        recognizer = Recognizer()
        recognizer.load_model(sample_rate=source.sample_rate)
        speech_stream = get_speech_sounds_observable(source=source)  # type: Observable
        rr_stream = speech_stream.pipe(
            op.map(recognizer.process_speech_sound),
            op.share()
        )
        rr_stream.subscribe(rx_nop, logger.exception)  # displays exceptions

        self.activation_command_stream, self.rr_stream = rr_stream.pipe(op.partition(lambda r: r.is_activation_command))

        active_rr_stream = self.rr_stream.pipe(
            op.filter(lambda r: is_ableton_focused()),
            op.filter(lambda r: SRConfig.SR_ACTIVE),
        )

        self.rr_error_stream, self.command_stream = active_rr_stream.pipe(op.partition(lambda r: r.error))
        self.speech_command_stream, self.ableton_command_stream = self.command_stream.pipe(
            op.partition(lambda r: isinstance(r.word_enum, SpeechCommandEnum)))
        self.displayable_stream = self.activation_command_stream.pipe(op.merge(self.rr_error_stream))


@log_exceptions
def recognize_speech():
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.SR_WINDOW_TITLE)
    stream_provider = StreamProvider()

    if SRConfig.EXPORT_RESULTS:
        stream_provider.rr_stream.subscribe(export_recognizer_result, logger.exception)

    stream_provider.activation_command_stream.subscribe(lambda r: process_speech_command(r.word_enum))  # always active
    stream_provider.speech_command_stream.subscribe(lambda r: process_speech_command(r.word_enum))
    stream_provider.ableton_command_stream.subscribe(lambda res: protocol0.execute_vocal_command(str(res)))

    if SRConfig.USE_GUI:
        from sr.display.speech_gui import display_recognizer_result
        stream_provider.displayable_stream.subscribe(display_recognizer_result, logger.exception)
