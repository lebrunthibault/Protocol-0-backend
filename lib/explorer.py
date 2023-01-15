import os
import re
from os.path import basename
from time import sleep

import win32gui

from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import (
    get_coords_for_color,
)
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.mouse.mouse import click, drag_to, move_to
from lib.process import kill_window_by_criteria
from lib.window.window import focus_window


def _compare_strings(s1: str, s2: str) -> int:
    words_1 = re.findall("\s+|\S+", s1)
    words_2 = re.findall("\s+|\S+", s2)

    for w1, w2 in zip(words_1, words_2):
        if w1 != w2:
            return 1 if w1 > w2 else -1

    for wo1, wo2, result in ((words_1, words_2, -1), (words_2, words_1, 1)):
        if len(wo1) > len(wo2):
            if wo1[len(wo2)] == " ":
                return result
            else:
                return -result

    return 0


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

    from loguru import logger
    logger.success(handle)
    return handle


def drag_file_to(file_path: str, dest_coords: Coords, drag_duration=0.5, close_window=True):
    handle = _open_explorer(file_path)
    x, y, w, h = win32gui.GetWindowRect(handle)

    folder_name = basename(os.path.split(file_path)[0])

    coords = retry(20, 0.1)(get_coords_for_color)(
        [
            PixelColorEnum.EXPLORER_SELECTED_ENTRY,
            PixelColorEnum.EXPLORER_SELECTED_ENTRY_LIGHT,
        ],
        box_coords=(x + 200, y + 200, x + 1000, y + 750),
    )
    move_to(coords)
    drag_to(dest_coords, duration=drag_duration)

    if close_window:
        kill_window_by_criteria(name=folder_name)
