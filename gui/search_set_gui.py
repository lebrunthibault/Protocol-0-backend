import PySimpleGUI as sg
from PySimpleGUI import WIN_CLOSED
from loguru import logger

from lib.ableton.ableton import focus_ableton
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import focus_window

WINDOW_TITLE = "search"
KEEP_WINDOW_IN_BACKGROUND = False
RELOAD_ON_STARTUP = False


def send_search(search):
    # type: (str) -> None
    logger.info(f"sending search {search} to api")
    # connect to script


def create_gui():
    # type: () -> None
    layout = [[sg.Input(key="input")]]
    window = sg.Window(WINDOW_TITLE, layout,
                       return_keyboard_events=True)

    while True:
        event, values = window.read()

        if not event or event == WIN_CLOSED:
            return

        if not event or event == WIN_CLOSED or event.split(":")[0] == "Escape":
            logger.debug("Escape pressed, exiting")
            break

        if len(event) == 1 and ord(event) == 13:
            if KEEP_WINDOW_IN_BACKGROUND:
                logger.debug("Enter pressed, clearing and focusing ableton")
                window["input"].update("")
                focus_ableton()
                continue
            else:
                logger.debug("Enter pressed, closing")
                break

        if len(event) == 1:
            search = values["input"]
            if len(search) >= 3:
                send_search(search)

    window.close()


def search_set_gui():
    # type: () -> None
    if not RELOAD_ON_STARTUP:
        handle = find_window_handle_by_enum(name=WINDOW_TITLE)
        if handle:
            focus_window(name=WINDOW_TITLE)
            return

    create_gui()
