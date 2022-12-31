from loguru import logger

from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import get_closest_color_at_pixel
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.mouse.mouse import click


def toggle_ableton_button(coords: Coords, activate: bool) -> None:
    closest_color = get_closest_color_at_pixel(coords)
    logger.debug("closest_color: %s" % closest_color)

    if (
        activate
        and closest_color == PixelColorEnum.BUTTON_DEACTIVATED
        or not activate
        and closest_color.is_button_activated
    ):
        logger.debug("color matching expectation, dispatching click")
        click(*coords)
    else:
        logger.info("color %s not matching expectation, skipping" % closest_color)
