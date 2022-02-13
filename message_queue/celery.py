import os
from typing import List

from celery import Celery

from gui.window.notification.notification_factory import NotificationFactory
from gui.window.prompt.prompt_factory import PromptFactory
from gui.window.select.select_factory import SelectFactory
from lib.enum.NotificationEnum import NotificationEnum

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('tasks', broker='redis://localhost')
app.control.purge()
app.conf.result_expires = 1


def check_celery_worker_status() -> bool:
    """ from https://stackoverflow.com/questions/8506914/detect-whether-celery-is-available-running """
    i = app.control.inspect()
    availability = i.ping()

    return availability is not None


@app.task
def prompt(question: str):
    PromptFactory.createWindow(message=question, notification_enum=NotificationEnum.INFO).display()


@app.task
def select(question: str, options: List[str], vertical=True):
    SelectFactory.createWindow(message=question, options=options, vertical=vertical).display()


@app.task()
def notification(message: str, notification_enum=NotificationEnum.INFO.value):
    NotificationFactory.createWindow(message=message, notification_enum=NotificationEnum[notification_enum]).display()


app.control.rate_limit('message_queue.celery.notification', '50/m')
