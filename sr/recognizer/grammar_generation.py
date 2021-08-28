import subprocess

from loguru import logger
from protocol0.enums.ActionEnum import ActionEnum
from protocol0.enums.TrackSearchKeywordEnum import TrackSearchKeywordEnum

from sr.enums.speech_command_enum import SpeechCommandEnum
from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def prepare_model_grammar() -> None:
    with open(SRConfig.KALDI_VOCABULARY_PATH, "w") as f:
        word_enum_classes = [
            ActionEnum,
            TrackSearchKeywordEnum,
            SpeechCommandEnum
        ]
        enums = sum([list(enum_class) for enum_class in word_enum_classes])
        f.write(" ".join([enum.name.lower() for enum in enums]))

    subprocess.run(
        [
            "bash",
            "-c",
            "source /home/thibault/.zshrc && cd '/mnt/c/Users/thiba/Google Drive/music/dev/protocol0_system/sr/grammar' && make prepare",
        ]
    )

    logger.info("grammar generated")
