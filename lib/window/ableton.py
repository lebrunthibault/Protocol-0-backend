import logging

import keyboard

from lib.click import pixel_has_color
from lib.enum.InterfaceColorEnum import InterfaceColorEnum
from lib.enum.PixelEnum import PixelEnum
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum

logger = logging.getLogger(__name__)


def show_plugins() -> None:
    logger.info("show plugins pressed")
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
        logger.info("keys dispatched")
        keyboard.press_and_release('ctrl+alt+p')


def is_device_view_visible() -> bool:
    return pixel_has_color(
        PixelEnum.SEPARATOR.value[0], PixelEnum.SEPARATOR.value[1], InterfaceColorEnum.SEPARATOR.value
    )


def show_device_view() -> None:
    if not is_device_view_visible():
        send_keys("+{TAB}")
