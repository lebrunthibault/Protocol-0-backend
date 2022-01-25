import os
from typing import List

from celery import Celery
from loguru import logger

from gui.window.notification.notification_factory import NotificationFactory
from gui.window.prompt.prompt_factory import PromptFactory
from gui.window.select.select_factory import SelectFactory
from lib.enum.NotificationEnum import NotificationEnum

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('tasks', broker='redis://localhost')


@app.task
def test():
    logger.info("hello")


@app.task
def prompt(question: str):
    PromptFactory.createWindow(message=question, notification_enum=NotificationEnum.INFO).display()


@app.task
def select(question: str, options: List[str], vertical=True):
    SelectFactory.createWindow(message=question, options=options, vertical=vertical).display()


@app.task
def notification(message: str, notification_enum=NotificationEnum.INFO.value):
    NotificationFactory.createWindow(message=message, notification_enum=NotificationEnum[notification_enum]).display()
