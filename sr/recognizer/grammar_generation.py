import subprocess

from loguru import logger

from sr.sr_config import SRConfig

logger = logger.opt(colors=True)


def prepare_model_grammar() -> None:
    vocabulary = " ".join([enum.name.lower() for enum in SRConfig.word_enums()])

    with open(SRConfig.KALDI_VOCABULARY_PATH, "w") as f:
        f.write(vocabulary)

    grammar_directory = "/mnt/c/Users/thiba/google_drive/music/dev/protocol0_system/sr/grammar"
    subprocess.run(
        [
            "bash",
            "-c",
            f"source /home/thibault/.zshrc && cd '{grammar_directory}' && make prepare",
        ]
    )

    logger.info("grammar generated")
