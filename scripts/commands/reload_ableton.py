import time

from lib.click import click
from lib.keys import send_keys
from lib.window.window import focus_ableton


def reload_ableton() -> None:
    focus_ableton()
    time.sleep(0.5)
    send_keys("^n")
    send_keys("ctrl+n")
    send_keys("{Right}")
    send_keys("{Right}")
    send_keys("{Right}")
    send_keys("{Right}")
    send_keys("{Enter}")
    send_keys("{Enter}")


def save_set_as_template():
    # first possible position
    click(x=703, y=363)  # click on File Folder
    click(x=1032, y=201)  # click on set as new
    time.sleep(0.05)

    # second position possible
    click(x=703, y=332)  # click on File Folder
    click(x=1032, y=203)  # click on set as new (2nd position)
    click(x=1032, y=230)  # click on set as new (2nd position)
    time.sleep(0.05)
    send_keys("{Enter}")
    time.sleep(0.2)
    send_keys("	{ESC}")
