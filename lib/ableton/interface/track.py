from time import sleep
from typing import Tuple

import pyautogui
from PIL import ImageGrab

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.interface_color_enum import InterfaceColorEnum
from lib.decorators import timing
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import click
from protocol0.application.command.ProcessBackendResponseCommand import (
    ProcessBackendResponseCommand,
)

Coords = Tuple[int, int]


@timing
def get_track_coords(pixel_color: InterfaceColorEnum) -> Coords:
    screen = ImageGrab.grab()

    header_offset = 45  # skip these pixels

    for i, coords in enumerate(list(screen.getdata())[1920 * header_offset : 1920 * 100]):
        if coords == pixel_color.to_tuple:
            return (i % 1920, (i // 1920) + header_offset)

    raise Protocol0Error(f"{pixel_color} not found")


def flatten_focused_track():
    x, y = get_track_coords(InterfaceColorEnum.TRACK_FOCUSED)

    # click on freeze track
    click(x, y, button=pyautogui.RIGHT)
    click(x + 50, y + 150, keep_position=False)

    sleep(0.2)
    # wait for track freeze
    while "Freeze..." in get_ableton_windows():
        sleep(0.2)

    # click on flatten
    click(x, y, button=pyautogui.RIGHT)
    click(x + 50, y + 170, keep_position=False)

    p0_script_client().dispatch(ProcessBackendResponseCommand("ok", res_type="flatten"))
