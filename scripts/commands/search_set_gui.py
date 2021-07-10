import logging

import PySimpleGUI as sg
import win32gui
from PySimpleGUI import WIN_CLOSED

from lib.window.find_window import find_window_handle_by_criteria
from lib.window.window import focus_ableton
from server.p0_script_api_client import p0_script_api_client

logger = logging.getLogger(__name__)

WINDOW_TITLE = "toto"
KEEP_WINDOW_IN_BACKGROUND = False
RELOAD_ON_STARTUP = False


def send_search(search):
    # type: (str) -> None
    logger.info(f"sending search {search} to api")
    p0_script_api_client.search_track(search=search)


def create_gui():
    # type: () -> None
    layout = [[sg.Input(key="input")]]
    window = sg.Window(WINDOW_TITLE, layout,
                       return_keyboard_events=True,
                       # no_titlebar=True,
                       )

    while True:
        event, values = window.read()

        if not event or event == WIN_CLOSED:
            return

        if not event or event == WIN_CLOSED or event.split(":")[0] == "Escape":
            logger.info("Escape pressed, exiting")
            break

        if len(event) == 1 and ord(event) == 13:
            if KEEP_WINDOW_IN_BACKGROUND:
                logger.info("Enter pressed, clearing and focusing ableton")
                window["input"].update("")
                focus_ableton()
                continue
            else:
                logger.info("Enter pressed, closing")
                break

        if len(event) == 1:
            search = values["input"]
            if len(search) >= 3:
                send_search(search)

    window.close()


def search_set_gui():
    # type: () -> None
    if not RELOAD_ON_STARTUP:
        search_window_handle = find_window_handle_by_criteria(partial_name=WINDOW_TITLE)
        if search_window_handle:
            logger.info("found search set window, focusing")
            win32gui.SetForegroundWindow(search_window_handle)
            return
        else:
            logger.info("didn't find search set window, creating gui")

    create_gui()
