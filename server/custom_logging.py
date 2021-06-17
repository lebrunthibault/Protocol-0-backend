import json
import logging
import sys
from functools import partial
from pathlib import Path
from pprint import pformat

from loguru import logger

from consts import LOGGING_DIRECTORY


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        message = record.getMessage()
        # truncating access logs
        if record.name == "uvicorn.access":
            message = message.split(" - ")[1]

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, message
        )


def format_record(record: dict, format_string: str) -> str:
    """
    Custom format for loguru loggers.
    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.

    Example:
    >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    >>> logger.bind(payload=).debug("users payload")
    >>> [   {   'count': 2,
    >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    if "uvicorn" in record['file'].path:
        format_string = format_string.replace(" - <cyan>{name}</cyan>:<cyan>{function}</cyan>", "")

        # format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


class CustomizeLogger:

    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')

        logger = cls.customize_logging(
            f"{LOGGING_DIRECTORY}\\{logging_config.get('filename')}",
            level=logging_config.get('level'),
            format_stdout=logging_config.get('format_stdout'),
            format_log_file=logging_config.get('format_log_file')
        )
        return logger

    @classmethod
    def customize_logging(cls,
                          filepath: str,
                          level: str,
                          format_stdout: str,
                          format_log_file: str
                          ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=False,
            level=level.upper(),
            filter=cls.filter_logs,
            format=partial(format_record, format_string=format_stdout)
        )

        logger.add(
            str(filepath),
            enqueue=True,
            backtrace=False,
            level=level.upper(),
            filter=partial(cls.filter_logs, is_log_file=True),
            format=partial(format_record, format_string=format_log_file)
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        # logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn.access",
                     'uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        config = None
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config

    @classmethod
    def filter_logs(cls, record, is_log_file=False) -> bool:
        # don't pollute web logs with server restarts
        if is_log_file:
            if any(
                    name in record['name'] for name in ["uvicorn.server", "uvicorn.lifespan"]):
                return False
            if record["extra"].get("stdout_only"):
                return False

        """ Here do not log polling from ableton """
        if "GET /action" in record['message']:
            return False
        else:
            return True
