import glob
import os
from os.path import basename
from typing import List

from api.settings import Settings
from lib.ableton.interface.coords import Coords, CoordsEnum
from lib.ableton.interface.explorer import sort_by_name
from lib.ableton.interface.pixel import get_absolute_coords, wait_for_pixel_color
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.decorators import retry
from lib.mouse.mouse import click
from lib.window.window import focus_window


class TrackFolder:
    def __init__(self, path: str):
        assert os.path.exists(path), f"'{path}' does not exist"

        self._path = path

    def click_track(self, track_name: str):
        """place cursor on track"""
        os.startfile(self._path)
        handle = retry(10, 0.1)(focus_window)(name=Settings().instrument_tracks_folder)

        coords = get_absolute_coords(handle, self._get_relative_coords(track_name))
        click(*coords, exact=True)
        wait_for_pixel_color(PixelColorEnum.EXPLORER_ABLETON_SET_ICON, coords)

    def _get_relative_coords(self, track_name: str) -> Coords:
        tracks = sort_by_name([basename(t).replace(".als", "") for t in self._saved_tracks])

        assert track_name in tracks, f"'{track_name}.als' does not exist"

        index = tracks.index(track_name)
        x, y = CoordsEnum.EXPLORER_FIRST_TRACK_ICON.value
        if index % 2 != 0:
            x += 385

        index //= 2

        return x, y + index * 40

    @property
    def _saved_tracks(self) -> List:
        return glob.glob(f"{self._path}\\*.als")
