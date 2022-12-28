from time import sleep

from gui.celery import notification_window
from lib.enum.notification_enum import NotificationEnum
from lib.keys import send_keys
from lib.mouse.mouse import click

DRUM_RACK_SAVE_BUTTON_WIDTH = 351
DRUM_RACK_SAVE_BUTTON_HEIGHT = 803


def save_drum_rack(drum_rack_name: str):
    notification_window.delay("Saving the drum rack", NotificationEnum.WARNING.value)
    click(DRUM_RACK_SAVE_BUTTON_WIDTH, DRUM_RACK_SAVE_BUTTON_HEIGHT)
    sleep(0.5)
    send_keys(drum_rack_name)
    sleep(0.5)
    send_keys("{ENTER}")
