from time import sleep

from lib.ableton.interface.coords import CoordsEnum
from lib.ableton.interface.pixel import get_closest_color_at_pixel
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.keys import send_keys, send_up, send_down, send_right
from lib.mouse.mouse import click, double_click


def toggle_browser():
    send_keys("^%b")
    sleep(0.1)


def is_browser_visible() -> bool:
    color = get_closest_color_at_pixel(CoordsEnum.BROWSER_LEFT_SIZE.value)
    return color == PixelColorEnum.BROWSER


def is_browser_tracks_folder_clickable(coords: CoordsEnum) -> bool:
    """Checks both that the browser is big enough and that the ableton proejct is not shown instead"""
    return get_closest_color_at_pixel(coords.value).is_browser_shown


def click_browser_tracks():
    if not is_browser_visible():
        toggle_browser()

    coords = CoordsEnum.BROWSER_PLACE_TRACKS

    if not is_browser_tracks_folder_clickable(coords):
        coords = CoordsEnum.BROWSER_PLACE_TRACKS_2
        # browser should have a minimum size
        assert is_browser_tracks_folder_clickable(coords), "Browser is not selectable"

    # drag the track to the tracks folder
    double_click(coords.value)


def search(search: str):
    send_keys("^f")
    sleep(0.1)
    send_keys(search)


def preload_sample_category(category: str):
    search("")  # focus the browser
    sleep(0.1)
    click(*CoordsEnum.BROWSER_PLACE_IMPORTED)  # click on samples folder in browser
    sleep(0.05)
    click(*CoordsEnum.BROWSER_SEARCH_BOX)  # click in the search box without activating search mode
    sleep(0.05)
    send_keys("^a")
    send_keys("{BACKSPACE}")
    send_keys(f"'{category}'")  # filter on the set folder
    sleep(0.2)

    # a way to always show the tracks sub folder
    send_down()

    send_right()
