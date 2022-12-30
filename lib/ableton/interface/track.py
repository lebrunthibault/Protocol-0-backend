from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.pixel import get_color_coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.mouse.mouse import click
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


def flatten_focused_track():
    x, y = get_color_coords(PixelColorEnum.TRACK_FOCUSED)

    # click on freeze track
    click(x, y, button=pyautogui.RIGHT)
    click(x + 50, y + 150)

    sleep(0.2)
    # wait for track freeze
    while "Freeze..." in get_ableton_windows():
        sleep(0.2)

    # click on flatten
    click(x, y, button=pyautogui.RIGHT)
    click(x + 50, y + 170)

    p0_script_client().dispatch(EmitBackendEventCommand("track_flattened"))
