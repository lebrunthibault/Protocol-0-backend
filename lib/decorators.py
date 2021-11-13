from functools import wraps

from loguru import logger

from api.p0_script_api_client import protocol0


def log_exceptions(func):
    @wraps(func)
    def decorate(*a, **k):
        # noinspection PyBroadException
        try:
            func(*a, **k)
        except Exception as e:
            logger.exception(e)
            pass
    return decorate


def reset_midi_client(func):
    @wraps(func)
    def decorate(*a, **k):
        # noinspection PyBroadException
        protocol0.IS_LIVE = False
        func(*a, **k)

    return decorate
