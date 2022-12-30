import enum
import glob
import os
from os.path import basename
from time import sleep
from typing import List

from api.settings import Settings
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.explorer import sort_by_name
from lib.ableton.interface.pixel import get_absolute_coords
from lib.decorators import retry
from lib.mouse.mouse import click
from lib.window.window import focus_window


class ExplorerDisplayEnum(enum.Enum):
    SMALL_ICONS = "SMALL_ICONS"
    DETAILS = "DETAILS"


class TrackFolder:
    def __init__(self, path: str, display: ExplorerDisplayEnum):
        assert os.path.exists(path), f"'{path}' does not exist"

        self._path = path
        self._display = display

    def click_track(self, track_name: str):
        """place cursor on track"""
        os.startfile(self._path)
        handle = retry(10, 0.1)(focus_window)(name=Settings().track_window_title)

        coords = self._get_relative_coords(track_name)
        click(*get_absolute_coords(handle, coords), exact=True)
        sleep(0.5)

    def _get_relative_coords(self, track_name: str) -> Coords:
        tracks = sort_by_name([basename(t).replace(".als", "") for t in self._saved_tracks])
        from loguru import logger

        logger.success(tracks)

        assert track_name in tracks, f"'{track_name}.als' does not exist"

        index = tracks.index(track_name)
        logger.success(index)
        x = 340

        if self._display == ExplorerDisplayEnum.SMALL_ICONS:
            if index % 2 != 0:
                x += 385

            index //= 2

        return x, 200 + index * 40

    @property
    def _saved_tracks(self) -> List:
        return glob.glob(f"{self._path}\\*.als")
