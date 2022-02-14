import os
import socket
from functools import wraps
from typing import List

from celery import Celery
from loguru import logger

from gui.window.notification.notification_factory import NotificationFactory
from gui.window.prompt.prompt_factory import PromptFactory
from gui.window.select.select_factory import SelectFactory
from lib.enum.NotificationEnum import NotificationEnum

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = Celery('tasks', broker='redis://localhost')
celery_app.control.purge()
celery_app.conf.result_expires = 1


def kill_all_running_workers():
    for worker in celery_app.control.inspect().active()[f"celery@{socket.gethostname()}"]:
        os.kill(worker["worker_pid"], 9)


def check_celery_worker_status() -> bool:
    """ from https://stackoverflow.com/questions/8506914/detect-whether-celery-is-available-running """
    i = celery_app.control.inspect()
    availability = i.ping()

    return availability is not None


def handle_error(func):
    @wraps(func)
    def decorate(*a, **k):
        # noinspection PyBroadException
        try:
            func(*a, **k)
        except Exception as e:
            logger.exception(e)
            notification.delay(str(e), NotificationEnum.ERROR.value)

    return decorate


@celery_app.task
@handle_error
def prompt(question: str):
    PromptFactory.createWindow(message=question, notification_enum=NotificationEnum.INFO).display()


@celery_app.task
@handle_error
def select(question: str, options: List[str], vertical=True):
    SelectFactory.createWindow(message=question, options=options, vertical=vertical).display()


@celery_app.task()
@handle_error
def notification(message: str, notification_enum=NotificationEnum.INFO.value):
    NotificationFactory.createWindow(message=message, notification_enum=NotificationEnum[notification_enum]).display()


celery_app.control.rate_limit('message_queue.celery.notification', '50/m')
