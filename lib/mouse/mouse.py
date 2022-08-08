import pyautogui
from PIL import ImageGrab
from loguru import logger
from typing import Tuple

from config import Config
from lib.enum.InterfaceColorEnum import InterfaceColorEnum


def move_to(x: int, y: int) -> None:
    pyautogui.moveTo(x, y)


def click(x: int, y: int, keep_position=False, exact=False) -> None:
    # coordinates are relative to a 1080p display resolution
    # accounting for resolution change
    if not exact:
        x *= Config.DISPLAY_RESOLUTION_FACTOR
        y *= Config.DISPLAY_RESOLUTION_FACTOR

    mouse_position = pyautogui.position()

    try:
        pyautogui.click(x, y)
    except pyautogui.FailSafeException as e:
        logger.warning(e)

    if keep_position:
        pyautogui.click(mouse_position)


def click_vertical_zone(x: int, y: int) -> None:
    for i in range(120, -40, -20):
        pyautogui.click(x, y + i)


def right_click(x: int, y: int) -> None:
    pyautogui.rightClick(x, y)


def double_click(x: int, y: int) -> None:
    pyautogui.doubleClick(x, y)


def get_pixel_color_at(x: int, y: int) -> Tuple[int, int, int]:
    image = ImageGrab.grab()
    pixel_color = image.getpixel((x, y))
    logger.debug("pixel_color: %s" % InterfaceColorEnum.get_string_from_tuple(pixel_color))
    return pixel_color
