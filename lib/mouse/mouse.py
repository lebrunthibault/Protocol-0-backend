from typing import Tuple

import pyautogui
from PIL import ImageGrab
from loguru import logger

from lib.enum.InterfaceColorEnum import InterfaceColorEnum


def move_to(x: int, y: int) -> None:
    pyautogui.moveTo(x, y)


def click(x: int, y: int) -> None:
    try:
        pyautogui.click(x, y)
    except pyautogui.FailSafeException as e:
        logger.warning(e)


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
