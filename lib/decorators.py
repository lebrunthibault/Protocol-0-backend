from datetime import datetime, timedelta
from functools import wraps

from loguru import logger

from api.p0_script_api_client import p0_script_client


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
        p0_script_client.IS_LIVE = False
        func(*a, **k)

    return decorate


class throttle(object):
    """
    Decorator that prevents a function from being called more than once every
    time period.
    To create a function that cannot be called more than once a minute:
        @throttle(minutes=1)
        def my_fun():
            pass
    """

    def __init__(self, milliseconds=0):
        self.throttle_period = timedelta(milliseconds=milliseconds)
        self.time_of_last_call = datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            time_since_last_call = datetime.now() - self.time_of_last_call

            if time_since_last_call <= self.throttle_period:
                logger.info(f"time_since_last_call: {time_since_last_call}: NOK")
                return

            res = fn(*args, **kwargs)
            self.time_of_last_call = datetime.now()
            return res

        return wrapper
