import logging

import pyautogui
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")

logger = logging.getLogger(__name__)


def send_keys(keys: str) -> None:
    logger.info("sending keys: %s" % keys)
    # keyboard.press_and_release()
    shell.SendKeys(keys, 0)


def send_hotkey(hotkey: str) -> None:
    logger.info("sending hotkey: %s" % hotkey)
    pyautogui.hotkey(*hotkey.split("+"))
