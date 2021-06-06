import logging

import keyboard
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum


def _show_plugins():
    logging.info("show plugins pressed")
    if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
        logging.info("keys dispatched")
        keyboard.press('ctrl+alt+p')


if __name__ == "__main__":
    import time

    start_time = time.monotonic()

    send_keys("a")
    # keyboard.press('a')

    print('seconds: ', time.monotonic() - start_time)
