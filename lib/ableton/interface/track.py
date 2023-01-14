from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import get_focused_track_coords, get_pixel_color_at
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.explorer import drag_file_to
from lib.mouse.mouse import click
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


def _click_context_menu(track_coords: Coords, y_offset: int):
    """handles when menu appears left or right"""
    x, y = track_coords
    click(x, y, button=pyautogui.RIGHT)
    menu_coords = (x + 10, y + y_offset)

    if get_pixel_color_at(menu_coords) != PixelColorEnum.TRACK_CONTEXT_MENU_BACKGROUND.rgb:
        menu_coords = (x - 10, y + y_offset)

    click(*menu_coords)


def flatten_track():
    coords = get_focused_track_coords()

    _click_context_menu(coords, 150)  # freeze track

    sleep(0.2)
    # wait for track freeze
    while "Freeze..." in get_ableton_windows():
        sleep(0.2)

    _click_context_menu(coords, 170)  # flatten track

    p0_script_client().dispatch(EmitBackendEventCommand("track_flattened"))


def load_instrument_track(instrument_name: str):
    track_path = f"{settings.ableton_set_directory}\\{settings.instrument_tracks_folder}\\{instrument_name}.als"

    drag_file_to(track_path, get_focused_track_coords(box_boundary="right"), drag_duration=0.2)

    p0_script_client().dispatch(EmitBackendEventCommand("instrument_loaded"))
