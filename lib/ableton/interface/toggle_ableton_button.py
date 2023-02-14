from loguru import logger

from lib.ableton.ableton import show_plugins
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import get_pixel_color_at
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.mouse.mouse import click


def toggle_ableton_button(coords: Coords, activate: bool) -> None:
    color = get_pixel_color_at(coords)

    logger.debug("color: %s" % color)

    if (
        activate
        and color == PixelColorEnum.BUTTON_DEACTIVATED
        or not activate
        and color.is_button_activated
    ):
        logger.debug("color matching expectation, dispatching click")
        click(coords)
    else:
        logger.info("color %s not matching expectation, skipping" % color)
        show_plugins()
