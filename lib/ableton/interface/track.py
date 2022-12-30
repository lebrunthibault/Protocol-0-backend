from time import sleep

import pyautogui

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.get_set import get_ableton_windows
from lib.ableton.interface.pixel import get_color_coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton.track_folder import TrackFolder
from lib.mouse.mouse import drag_to, click
from lib.process import kill_window_by_criteria
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


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


def load_instrument_track(instrument_name: str):
    track_folder = TrackFolder(
        f"{settings.ableton_set_directory}\\{settings.instrument_tracks_folder}"
    )
    track_folder.click_track(instrument_name)

    drag_to(get_color_coords(PixelColorEnum.TRACK_FOCUSED, box_boundary="right"), duration=0.2)

    # remove the explorer window
    kill_window_by_criteria(name=settings.instrument_tracks_folder)
    p0_script_client().dispatch(EmitBackendEventCommand("instrument_loaded"))
