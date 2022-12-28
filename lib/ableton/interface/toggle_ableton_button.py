from loguru import logger

from lib.ableton.ableton import get_closest_color_at_pixel
from lib.ableton.interface.interface_color_enum import InterfaceColorEnum
from lib.mouse.mouse import click


def toggle_ableton_button(x: int, y: int, activate: bool) -> None:
    closest_color = get_closest_color_at_pixel(x, y)
    logger.debug("closest_color: %s" % closest_color)

    if (
        activate
        and closest_color == InterfaceColorEnum.BUTTON_DEACTIVATED
        or not activate
        and closest_color.button_activated
    ):
        logger.debug("color matching expectation, dispatching click")
        click(x, y)
    else:
        logger.info("color %s not matching expectation, skipping" % closest_color)
