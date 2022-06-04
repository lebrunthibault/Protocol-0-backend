import os
import sys
from functools import wraps
from typing import List

from celery import Celery
from loguru import logger

from gui.task_cache import TaskCache, TaskCacheKey
from gui.window.message.message_factory import MessageFactory
from gui.window.notification.notification_factory import NotificationFactory
from gui.window.prompt.prompt_factory import PromptFactory
from gui.window.select.select_factory import SelectFactory
from lib.enum.NotificationEnum import NotificationEnum

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_app = Celery('tasks', broker='redis://localhost')
celery_app.control.purge()
celery_app.conf.result_expires = 1

task_cache = TaskCache()


def revoke_tasks(task_type: TaskCacheKey):
    for task_id in task_cache.get_tasks(task_type):
        task_cache.add_revoked_task(task_id)
    task_cache.clear_tasks(task_type)


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
            message_window.delay(str(e), NotificationEnum.ERROR.value)

    return decorate


@celery_app.task(bind=True)
@handle_error
def notification_window(self, message: str, notification_enum: str = NotificationEnum.INFO.value, centered=False):
    revoke_tasks(TaskCacheKey.NOTIFICATION)
    task_cache.add_task(TaskCacheKey.NOTIFICATION, self.request.id)
    NotificationFactory.createWindow(
        message=message,
        notification_enum=NotificationEnum[notification_enum],
        centered=centered)\
        .display(self.request.id)


@celery_app.task()
@handle_error
def message_window(message: str, notification_enum: str = NotificationEnum.INFO.value):
    MessageFactory.createWindow(message=message, notification_enum=NotificationEnum[notification_enum]).display()


@celery_app.task
@handle_error
def prompt_window(question: str):
    PromptFactory.createWindow(message=question, notification_enum=NotificationEnum.INFO).display()


@celery_app.task
@handle_error
def select_window(question: str, options: List, vertical=True):
    SelectFactory.createWindow(message=question, options=options, vertical=vertical).display()
