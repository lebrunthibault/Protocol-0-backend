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
            get_selected_track_header_coordinates(exclude_left_track=False)
            return
        except Protocol0Error:
            sleep(0.1)


@timing
def get_selected_track_header_coordinates(exclude_left_track=True) -> Tuple[int, int]:
    screen = ImageGrab.grab(bbox=None)

    # a = np.argwhere(screen.getdata() == (199, 237, 255))
    res = None

    for i, coords in enumerate(screen.getdata()):
        y = i // 1920

        if y >= 100:
            break

        if coords == (199, 237, 255):
            res = (i % 1920, y)
            break

    if res is None:
        raise Protocol0Error("No selected track")
    elif exclude_left_track and res == (44, 49):  # the focused track is still the drums track
        raise Protocol0Error("Too fast: retry")

    return res
