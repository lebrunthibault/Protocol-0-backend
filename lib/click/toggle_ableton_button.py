import math
from typing import Tuple

from loguru import logger

from lib.click.click import click, get_pixel_color
from lib.enum.InterfaceColorEnum import InterfaceColorEnum


def _distance(c1, c2):
    # type: (Tuple[int, int, int], Tuple[int, int, int]) -> float
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def _get_closest_color_at_pixel(x, y):
    # type: (int, int) -> InterfaceColorEnum
    return sorted(list(InterfaceColorEnum), key=lambda c: _distance(c.get_tuple(), get_pixel_color(x, y)))[0]


def toggle_ableton_button(x: int, y: int, activate: bool) -> None:
    closest_color = _get_closest_color_at_pixel(x, y)
    logger.debug("closest_color: %s" % closest_color)
    if (activate and closest_color != InterfaceColorEnum.ACTIVATED) or (
        not activate and closest_color == InterfaceColorEnum.ACTIVATED
    ):
        logger.debug("color matching expectation, dispatching click")
        click(x, y)
    else:
        logger.info("color %s not matching expectation, skipping" % closest_color)
