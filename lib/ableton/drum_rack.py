from time import sleep

from gui.celery import notification_window
from lib.enum.notification_enum import NotificationEnum
from lib.keys import send_keys
from lib.mouse.mouse import click


def save_drum_rack(drum_rack_name: str):
    notification_window.delay("Saving the drum rack", NotificationEnum.WARNING.value)
    click((351, 803))
    sleep(0.5)
    send_keys(drum_rack_name)
    sleep(0.5)
    send_keys("{ENTER}")
