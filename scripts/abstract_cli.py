import traceback

from loguru import logger

from lib.log import configure_logging


def _exception_handler(_, value, tb):
    logger.error(f"{value}\n")
    if tb:
        format_exception = traceback.format_tb(tb)
        for line in format_exception:
            logger.error(repr(line))


def setup_cli():
    # sys.excepthook = _exception_handler
    configure_logging()
    # configure_logging(filename="cli.log")
