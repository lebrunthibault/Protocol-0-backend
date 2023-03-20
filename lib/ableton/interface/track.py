from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings, DOWN_BBOX
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import get_pixel_color_at, get_coords_for_color
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.explorer import drag_file_to
from lib.mouse.mouse import click
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


def get_focused_track_coords(box_boundary="left") -> Coords:
    x, y = get_coords_for_color(
        [PixelColorEnum.ELEMENT_FOCUSED, PixelColorEnum.ELEMENT_SELECTED],
        bbox=(40, 45, 1870, 110),
        from_right=box_boundary == "right",
    )
    p0_script_client().dispatch(EmitBackendEventCommand("track_focused"))

    return x, y + 5  # drag works better here


def _click_context_menu(track_coords: Coords, y_offset: int):
    """handles when menu appears left or right"""
    click(track_coords, button=pyautogui.RIGHT)

    x, y = track_coords

    menu_coords = (x + 10, y + y_offset)

    if get_pixel_color_at(menu_coords) != PixelColorEnum.CONTEXT_MENU_BACKGROUND:
        menu_coords = (x - 10, y + y_offset)

    click(menu_coords)


def flatten_track(is_only_child):
    freeze_pos = 150
    if is_only_child:
        freeze_pos = 111

    coords = get_focused_track_coords()

    _click_context_menu(coords, freeze_pos)  # freeze track
    sleep(0.2)

    # wait for track freeze
    while "Freeze..." in get_ableton_windows():
        sleep(0.2)

    sleep(0.3)

    _click_context_menu(coords, freeze_pos + 20)  # flatten track

    p0_script_client().dispatch(EmitBackendEventCommand("track_flattened"))


def load_instrument_track(instrument_name: str):
    track_path = f"{settings.ableton_set_directory}\\{settings.instrument_tracks_folder}\\{instrument_name}.als"

    drag_file_to(
        track_path,
        get_focused_track_coords(box_boundary="right"),
        bbox=DOWN_BBOX,
        drag_duration=0.2,
    )

    p0_script_client().dispatch(EmitBackendEventCommand("instrument_loaded"))


def click_focused_track():
    coords = get_focused_track_coords(box_boundary="right")
    click(coords)
    p0_script_client().dispatch(EmitBackendEventCommand("track_clicked"))
