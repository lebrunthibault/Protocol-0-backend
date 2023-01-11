import os
from os.path import basename
from time import sleep

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.interface.pixel import (
    get_coords_for_color,
)
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import click, keep_mouse_position, drag_to, move_to
from lib.process import kill_window_by_criteria
from lib.window.window import focus_window
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def load_sample_in_simpler(sample_path: str):
    click(0, 500)  # move the cursor from the explorer window position
    folder_name = basename(os.path.split(sample_path)[0])
    try:
        focus_window(folder_name)
        sleep(0.1)
    except (AssertionError, Protocol0Error):
        os.system(f"explorer.exe /select, {sample_path}")
        handle = retry(50, 0.1)(focus_window)(name=folder_name)
        sleep(0.5)

    coords = get_coords_for_color(
        [
            PixelColorEnum.EXPLORER_SELECTED_ENTRY,
            PixelColorEnum.EXPLORER_SELECTED_ENTRY_LIGHT,
            PixelColorEnum.EXPLORER_SELECTED_ENTRY_DISABLED,
        ],
        height_offset=335,
        width_offset=590
    )
    move_to(coords)
    drag_to((55, 800), duration=0.5)
    kill_window_by_criteria(name=folder_name)
    p0_script_client().dispatch(EmitBackendEventCommand("sample_loaded"))

