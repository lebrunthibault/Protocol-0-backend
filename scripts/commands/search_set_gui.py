import PySimpleGUI as sg
from PySimpleGUI import WIN_CLOSED
from loguru import logger

from api.p0_script_api_client import p0_script_client
from lib.ableton import focus_ableton
from lib.window.window import focus_window

WINDOW_TITLE = "search"
KEEP_WINDOW_IN_BACKGROUND = False
RELOAD_ON_STARTUP = False


def send_search(search):
    # type: (str) -> None
    logger.info(f"sending search {search} to api")
    p0_script_client.search_track(search=search)


def create_gui():
    # type: () -> None
    logger.info("creating gui")
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
        if focus_window(name=WINDOW_TITLE):
            return

    create_gui()
