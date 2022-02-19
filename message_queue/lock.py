import time
from contextlib import contextmanager
from django.core.cache import cache
from loguru import logger

cache = {
    "notification": []
}

LOCK_EXPIRE = 10  # Lock expires in 10 seconds


@contextmanager
def task_lock(lock_id):
    """ cf : https://docs.celeryproject.org/en/latest/tutorials/task-cookbook.html#ensuring-a-task-is-only-executed-one-at-a-time """
    timeout_at = time.monotonic() + LOCK_EXPIRE
    logger.info(f"timeout_at: {timeout_at}")
    # cache.add fails if the key already exists
    expire = cache.get(lock_id, None)

    status = expire is None or expire >= time.monotonic()
    logger.info(f"expire: {expire}")
    logger.info(f"status: {status}")

    if status:
        cache[lock_id] = timeout_at

    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            del cache[lock_id]
