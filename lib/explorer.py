import os
from os.path import basename
from time import sleep

from lib.ableton.interface.coords import Coords, RectCoords
from lib.ableton.interface.pixel import (
    get_coords_for_color,
)
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import click, drag_to, move_to
from lib.process import kill_window_by_criteria
from lib.window.window import focus_window, move_window


def _open_explorer(file_path: str) -> int:
    assert os.path.exists(file_path), f"'{file_path}' does not exist"

    click(0, 500)  # move the cursor from the explorer window position
    folder_name = basename(os.path.split(file_path)[0])
    try:
        handle = focus_window(folder_name)
        sleep(0.1)
        return handle
    except (AssertionError, Protocol0Error):
        os.system(f"explorer.exe /select, {file_path}")
        handle = retry(50, 0.1)(focus_window)(name=folder_name)
        sleep(0.5)

    return handle


def drag_file_to(
    file_path: str,
    dest_coords: Coords,
    drag_duration=0.5,
    close_window=True,
    rect_coords: RectCoords = None,
):
    handle = _open_explorer(file_path)

    # by default: window at the bottom left
    rect_coords = rect_coords or (0, 330, 1100, 750)
    x, y, w, h = rect_coords

    move_window(handle, x, y, w, h)

    folder_name = basename(os.path.split(file_path)[0])

    coords = retry(20, 0.1)(get_coords_for_color)(
        [
            PixelColorEnum.EXPLORER_SELECTED_ENTRY,
            PixelColorEnum.EXPLORER_SELECTED_ENTRY_LIGHT,
        ],
        box_coords=(x + 200, y + 200, x + w, y + h),
    )
    move_to(coords)
    drag_to(dest_coords, duration=drag_duration)

    if close_window:
        kill_window_by_criteria(name=folder_name)
