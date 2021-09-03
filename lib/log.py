import json
import sys
from typing import Optional

from loguru import logger

from config import SystemConfig


def configure_logging(filename: Optional[str] = None) -> None:
    with open(f"{SystemConfig.PROJECT_ROOT}/lib/logging_config.json") as config_file:
        logging_config = json.load(config_file)

    logger.remove()
    logger.add(
        sys.stdout,
        level=logging_config.get("level"),
        format=logging_config.get("format_stdout"),
    )

    if filename:
        logger.add(
            f"{SystemConfig.LOGGING_DIRECTORY}\\{filename}",
            level=logging_config.get("level"),
            format=logging_config.get("format_log_file"),
        )
