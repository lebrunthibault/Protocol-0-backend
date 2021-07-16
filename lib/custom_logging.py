import json
import sys

from loguru import logger

from config import Config
from lib.consts import PROJECT_ROOT


def configure_logging(filename: str) -> None:
    with open(f"{PROJECT_ROOT}/server/logging_config.json") as config_file:
        logging_config = json.load(config_file)

    logger.remove()
    logger.add(
        sys.stdout,
        level=logging_config.get("level"),
        format=logging_config.get("format_stdout"),
    )

    logger.add(
        f"{Config.LOGGING_DIRECTORY}\\{filename}",
        level=logging_config.get("level"),
        format=logging_config.get("format_log_file"),
        colorize=True
    )
