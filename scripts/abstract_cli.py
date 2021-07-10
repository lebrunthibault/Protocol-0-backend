import sys
import traceback

import click_completion
from loguru import logger

from lib.custom_logging import configure_logging


def _exception_handler(exctype, value, tb):
    logger.error(f"{value}\n")
    if tb:
        format_exception = traceback.format_tb(tb)
        for line in format_exception:
            logger.error(repr(line))


def setup_cli():
    sys.excepthook = _exception_handler
    click_completion.init()
    configure_logging(filename="cli.log")
