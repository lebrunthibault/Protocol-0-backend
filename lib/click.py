from typing import Tuple

import pyautogui
import win32api
from PIL import ImageGrab
from loguru import logger

from lib.enum.InterfaceColorEnum import InterfaceColorEnum


def click(x: int, y: int, double_click: bool = False, back_to_previous_position: bool = False) -> None:
    (orig_x, orig_y) = win32api.GetCursorPos()
    logger.info("clicking at x: %s, y: %s" % (x, y))
    if double_click:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.click(x, y)
    if back_to_previous_position:
        win32api.SetCursorPos((orig_x, orig_y))


def get_pixel_color(x: int, y: int) -> Tuple[int, int, int]:
    image = ImageGrab.grab()
    pixel_color = image.getpixel((x, y))
    logger.info("pixel_color: %s" % InterfaceColorEnum.get_string_from_tuple(pixel_color))
    return pixel_color


def pixel_has_color(x: int, y: int, color: str) -> bool:
    res = InterfaceColorEnum.get_tuple_from_string(color) == get_pixel_color(x, y)
    logger.info("pixel_has_color -> x: %s, y: %s, color: %s, res: %s" % (x, y, color, res))
    return res
