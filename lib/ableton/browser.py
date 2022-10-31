from time import sleep

from lib.ableton.ableton import toggle_fold_set
from lib.keys import send_keys, send_up, send_down, send_left, send_right
from lib.mouse.mouse import click


def search(search: str):
    send_keys("^f")
    sleep(0.1)
    send_keys(search)


def load_rev2_track():
    search('"Default.als"')
    sleep(0.2)
    send_down()
    send_down()
    send_right()

    for _ in range(12):
        send_down()

    send_up()
    send_up()

    send_keys("{ENTER}")


def load_minitaur_track():
    search('"Default.als"')
    sleep(0.2)

    send_down()
    send_down()
    send_right()

    for _ in range(12):
        send_down()

    send_up()

    send_keys("{ENTER}")


def preload_set_tracks(set_title: str):
    toggle_fold_set()

    search("")  # focus the browser
    send_keys("{BACKSPACE}")
    click(58, 500)  # click on "splurges" in browser
    sleep(0.05)
    click(86, 58)  # click in the search box without activating search mode
    sleep(0.05)

    send_keys(set_title)  # filter on the set folder

    # a way to always show the tracks sub folder
    send_down()
    send_down()

    send_left()
    send_left()
    send_left()
    send_left()
    send_left()
    send_left()
    send_left()

    send_right()

    send_down()
    send_down()

    send_right()
    send_down()
    send_right()
    send_down()
    send_right()
