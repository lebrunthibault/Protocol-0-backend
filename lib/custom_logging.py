import json
import os
import sys

from loguru import logger

from consts import LOGGING_DIRECTORY
from server.main import config_path


def configure_logging(filename: str) -> None:
    with open(config_path) as config_file:
        logging_config = json.load(config_file)

    os.environ["LOGURU_COLORIZE"] = "true"
    logger.remove()
    logger.add(
        sys.stdout,
        level=logging_config.get("level"),
        format=logging_config.get("format_stdout"),
    )

    logger.add(
        f"{LOGGING_DIRECTORY}\\cli.log",
        level=logging_config.get("level"),
        format=logging_config.get("format_log_file"),
        colorize=True
    )
