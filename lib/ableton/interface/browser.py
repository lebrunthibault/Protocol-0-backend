from time import sleep

from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton.interface.pixel import get_closest_color_at_pixel
from lib.ableton_set import AbletonSet
from lib.keys import send_keys, send_up, send_down, send_right
from lib.mouse.mouse import click


def toggle_browser():
    send_keys("^%b")
    sleep(0.1)


def is_browser_visible() -> bool:
    color = get_closest_color_at_pixel(18, 221)
    return color == PixelColorEnum.BROWSER


def is_browser_tracks_folder_clickable() -> bool:
    color = get_closest_color_at_pixel(27, 502)

    return color.browser_shown


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


def preload_set_tracks(set: AbletonSet):
    if not is_browser_visible():
        toggle_browser()
    assert is_browser_tracks_folder_clickable(), "Browser is not selectable"

    click(50, 474)  # click on "tracks" in browser


def preload_sample_category(category: str):
    search("")  # focus the browser
    sleep(0.1)
    click(58, 523)  # click on samples folder in browser
    sleep(0.05)
    click(86, 58)  # click in the search box without activating search mode
    sleep(0.05)
    send_keys("^a")
    send_keys("{BACKSPACE}")
    send_keys(f"'{category}'")  # filter on the set folder
    sleep(0.2)

    # a way to always show the tracks sub folder
    send_down()

    send_right()
