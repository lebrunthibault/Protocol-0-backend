import pyautogui
from PIL import ImageGrab
from loguru import logger
from typing import Tuple

from api.settings import Settings
from lib.enum.InterfaceColorEnum import InterfaceColorEnum


def move_to(x: int, y: int) -> None:
    pyautogui.moveTo(x, y)


def click(x: int, y: int, keep_position=True, exact=False) -> None:
    # coordinates are relative to a 1080p display resolution
    # accounting for resolution change
    if not exact:
        x *= Settings().display_resolution_factor
        y *= Settings().display_resolution_factor

    mouse_position = pyautogui.position()

    try:
        pyautogui.click(x, y)
    except pyautogui.FailSafeException as e:
        logger.warning(e)

    if keep_position:
        pyautogui.moveTo(mouse_position)


def click_vertical_zone(x: int, y: int) -> None:
    for i in range(120, -40, -20):
        pyautogui.click(x, y + i)


def get_pixel_color_at(x: int, y: int) -> Tuple[int, int, int]:
    image = ImageGrab.grab()
    pixel_color = image.getpixel((x, y))
    logger.debug("pixel_color: %s" % InterfaceColorEnum.get_string_from_tuple(pixel_color))
    return pixel_color
