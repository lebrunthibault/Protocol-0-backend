from loguru import logger

from lib.window.window import focus_window, focus_ableton
from sr.enums.speech_command_enum import SpeechCommandEnum
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def _activate_sr():
    logger.info("<red>Activating SR</>")
    SRConfig.SR_ACTIVE = True


def _pause_sr():
    logger.info("<red>Pausing SR</>")
    SRConfig.SR_ACTIVE = False


def _focus_log_window():
    focus_window(name=SRConfig.WINDOW_TITLE)


def _focus_ableton():
    logger.info("Focusing log window")
    focus_window(name=SRConfig.WINDOW_TITLE)


speech_command_mapping = {
    SpeechCommandEnum.PROTOCOL: _activate_sr,
    SpeechCommandEnum.PAUSE: _pause_sr,
    SpeechCommandEnum.EXIT: _pause_sr,
    SpeechCommandEnum.LOG: lambda: focus_window(name=SRConfig.WINDOW_TITLE),
    SpeechCommandEnum.MUSIC: focus_ableton,
}


def process_speech_command(speech_command: SpeechCommandEnum):
    if speech_command not in speech_command_mapping:
        logger.warning(f"{speech_command} not present in speech_command_mapping")
        return

    speech_command_mapping[speech_command]()
