from time import sleep

import pyautogui

from lib.ableton.interface.pixel import get_pixel_having_color, get_coords_for_color
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.keys import send_keys
from lib.mouse.mouse import click, keep_mouse_position, get_mouse_position


@keep_mouse_position
def toggle_clip_notes():
    click((87, 1015))


@keep_mouse_position
def edit_automation_value():
    x, y = get_mouse_position()

    click((x, y), button=pyautogui.RIGHT)

    possible_menu_heights = [527, 510, 472, 416, 397, 396, 366, -2]

    coords = []

    for height in reversed(sorted(possible_menu_heights)):
        # left and right
        coords += [(x - 10, y - height), (x + 10, y - height)]

    border_coords = get_pixel_having_color(coords, PixelColorEnum.BLACK, False)

    if border_coords is None:
        return

    x_border, y_border = border_coords

    click((x_border, y_border + 10))


def set_envelope_loop_length(length: int):
    coords = get_coords_for_color(
        [PixelColorEnum.BUTTON_ACTIVATED_YELLOW],
        bbox=(100, 500, 500, 1030),
        from_bottom=True,
        from_right=True,
    )

    click(coords)
    x, y = coords

    # set the length
    click((x + 30, y))
    sleep(0.05)
    send_keys(str(length))
    sleep(0.05)
    send_keys("{ENTER}")
