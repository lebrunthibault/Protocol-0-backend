import logging

import keyboard
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


def show_plugins():
    logging.info("show plugins pressed")
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
        logging.info("keys dispatched")
        keyboard.press_and_release('ctrl+alt+p')
