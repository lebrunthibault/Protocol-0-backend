from loguru import logger

from api.client.p0_script_api_client import p0_script_client
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel import get_pixel_color_at
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.mouse.mouse import click, keep_mouse_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def toggle_ableton_button(coords: Coords, activate: bool) -> None:
    color = get_pixel_color_at(coords)

    logger.info(f"color: {color}")
    logger.info(f"coords: {coords}")
    logger.success(activate)

    if (
        activate
        and color == PixelColorEnum.BUTTON_DEACTIVATED
        or not activate
        and color
        in (
            PixelColorEnum.BUTTON_ACTIVATED,
            PixelColorEnum.BUTTON_ACTIVATED_2,
            # PixelColorEnum.BUTTON_NOT_SHOWN,
        )
    ):
        logger.debug("color matching expectation, dispatching click")
        click(coords, duration=0.1)
    else:
        logger.info("color %s not matching expectation, skipping" % color)
        # show_plugins()

    p0_script_client().dispatch(EmitBackendEventCommand("button_toggled"))
