import subprocess

from loguru import logger

from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def prepare_model_grammar() -> None:
    vocabulary = " ".join([enum.name.lower() for enum in SRConfig.word_enums()])

    with open(SRConfig.KALDI_VOCABULARY_PATH, "w") as f:
        f.write(vocabulary)

    subprocess.run(
        [
            "bash",
            "-c",
            "source /home/thibault/.zshrc && cd '/mnt/c/Users/thiba/Google Drive/music/dev/protocol0_system/sr/grammar' && make prepare",
        ]
    )

    logger.info("grammar generated")
