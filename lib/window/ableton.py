import logging

import keyboard

from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum

logger = logging.getLogger(__name__)


def show_plugins() -> None:
    logger.info("show plugins pressed")
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
        logger.info("keys dispatched")
        keyboard.press_and_release('ctrl+alt+p')
