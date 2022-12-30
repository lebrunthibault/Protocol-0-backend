from functools import wraps

import pyautogui
from loguru import logger

from api.settings import Settings
from lib.ableton.interface.coords import Coords


def move_to(coords: Coords) -> None:
    pyautogui.moveTo(*coords)


def tween(n: float) -> float:
    """mouse go fast then slow"""
    return 1 - pow(n - 1, 6)


def drag_to(coords: Coords, duration=0.5) -> None:
    pyautogui.dragTo(*coords, button="left", duration=duration, tween=tween)


def click(x: int, y: int, exact=False, button=pyautogui.PRIMARY) -> None:
    # coordinates are relative to a 1080p display resolution
    # accounting for resolution change

    if not exact:
        x *= Settings().display_resolution_factor
        y *= Settings().display_resolution_factor

    try:
        pyautogui.click(x, y, button=button)
    except pyautogui.FailSafeException as e:
        logger.warning(e)


def click_vertical_zone(coords: Coords) -> None:
    x, y = coords
    for i in range(120, -40, -20):
        pyautogui.click(x, y + i)


def keep_mouse_position(func):
    @wraps(func)
    def decorate(*a, **k):
        coords = pyautogui.position()

        res = func(*a, **k)

        move_to(coords)

        return res

    return decorate
