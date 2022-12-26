from time import sleep
from typing import Tuple

from PIL import ImageGrab

from lib.decorators import timing
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import click, keep_mouse_position


@keep_mouse_position
def focus_left_most_track():
    for i in range(0, 6):
        click(70, 60, keep_position=False)
        try:
            get_selected_track_header_coordinates(find_left_track=True)
            return
        except Protocol0Error:
            sleep(0.1)


@timing
def get_selected_track_header_coordinates(find_left_track=False) -> Tuple[int, int]:
    screen = ImageGrab.grab()

    res = None

    for i, coords in enumerate(screen.getdata()):
        y = i // 1920

        if y >= 100:
            break

        if find_left_track and (i % 1920) > 100:
            continue

        if coords == (199, 237, 255):
            res = (i % 1920, y)
            break

    if res is None:
        raise Protocol0Error("No selected track")
    elif not find_left_track and res == (44, 49):  # the focused track is still the drums track
        raise Protocol0Error("Too fast: retry")

    return res
