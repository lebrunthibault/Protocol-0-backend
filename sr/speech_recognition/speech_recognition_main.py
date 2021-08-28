import ctypes

from loguru import logger
from p0_script_api import DefaultApi
from rx import operators as op, Observable

from sr.audio.source.microphone import Microphone
from sr.audio.speech_sound import get_speech_sounds_observable
from sr.enums.speech_command_enum import SpeechCommandEnum
from sr.recognizer.recognizer import Recognizer
from sr.recognizer.recognizer_result import export_recognizer_result
from sr.rx.rx_utils import rx_nop
from sr.speech_recognition.speech_command_manager import process_speech_command
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def recognize_speech():
    # from sr.display.speech_gui import SpeechGui  # for performance
    # SpeechGui.display_recognizer_result("toto")
    # return
    p0_script_api = DefaultApi()
    ctypes.windll.kernel32.SetConsoleTitleW(SRConfig.WINDOW_TITLE)
    source = Microphone()
    recognizer = Recognizer()
    recognizer.load_model(sample_rate=source.sample_rate)
    speech_stream = get_speech_sounds_observable(source=source)  # type: Observable
    rr_stream = speech_stream.pipe(
        op.map(recognizer.process_speech_sound),
        op.share()
    )

    if SRConfig.EXPORT_RESULTS:
        rr_stream.subscribe(export_recognizer_result, logger.exception)

    rr_stream.subscribe(rx_nop, logger.exception)  # displays exceptions

    rr_stream.pipe(
        op.filter(lambda r: isinstance(r.word_enum, SpeechCommandEnum)),
        op.map(lambda r: r.word_enum)
    ).subscribe(process_speech_command)

    active_rr_stream = rr_stream.pipe(op.filter(lambda r: SRConfig.SR_ACTIVE or r.is_activation_command))
    # if SRConfig.DEBUG:
    #     speech_stream.subscribe(audio_plot_sound, logger.exception)

    rr_ableton_stream = rr_stream.pipe(
        op.filter(lambda r: SRConfig.SR_ACTIVE and not r.error and not isinstance(r.word_enum, SpeechCommandEnum)))
    rr_ableton_stream.subscribe(lambda res: p0_script_api.execute_command(str(res)))

    if SRConfig.USE_GUI:
        from sr.display.speech_gui import SpeechGui  # for performance

        active_rr_stream.subscribe(SpeechGui.display_recognizer_result, logger.exception)
