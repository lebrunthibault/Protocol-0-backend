import time

import keyboard

from lib.window.window import focus_ableton


def reload_ableton() -> None:
    focus_ableton()
    time.sleep(0.5)
    # send_keys("^n")
    keyboard.press_and_release("ctrl+n")
    # send_keys("{Right}")
    # send_keys("{Right}")
    # send_keys("{Right}")
    # send_keys("{Right}")
    # send_keys("{Enter}")
    # send_keys("{Enter}")
