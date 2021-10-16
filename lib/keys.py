import win32com.client

from loguru import logger

shell = win32com.client.Dispatch("WScript.Shell")


def send_keys(keys: str) -> None:
    """ https://win32com.goermezer.de/microsoft/windows/controlling-applications-via-sendkeys.html """
    logger.info("sending keys: %s" % keys)
    # keyboard.press_and_release()
    shell.SendKeys(keys, 0)
