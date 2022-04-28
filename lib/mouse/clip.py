import time

from lib.keys import send_keys
from lib.mouse.mouse import click

DRUM_RACK_SAVE_BUTTON_WIDTH = 548
DRUM_RACK_SAVE_BUTTON_HEIGHT = 874


def set_clip_envelope_bar_length(length: int):
    click(548, 837)  # envelope view activation
    time.sleep(0.1)
    click(548, 874)  # unlink the envelope
    time.sleep(0.2)
    click(616, 876)  # the envelope loop length
    time.sleep(0.2)
    send_keys(str(length))
    time.sleep(0.1)
    send_keys("{Enter}")
