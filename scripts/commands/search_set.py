import logging

import PySimpleGUI as sg
import win32gui

from lib.window.find_window import find_window_handle_by_criteria
from lib.window.window import focus_ableton
from server.p0_script_api_client import p0_script_api_client

logger = logging.getLogger(__name__)

KEEP_WINDOW_IN_BACKGROUND = False
RELOAD_ON_STARTUP = True


def send_search(search):
    # type: (str) -> None
    logger.info(f"sending search {search} to api")
    p0_script_api_client.search_track(search=search)


#
# def create_vocal():
#     # sr.Microphone.list_microphone_names()
#     with mic as source:
#         print("starting recording")
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source)
#         print(audio)
#         s = r.recognize_google(audio, language="fr-FR")
#         print(s)


def create_gui():
    # type: () -> None
    layout = [[sg.Input(key="input")]]
    window = sg.Window("", layout, return_keyboard_events=True, no_titlebar=True)
    # speech_recognition = SpeechRecognition()

    while True:
        event, values = window.read()
        if event.split(":")[0] == "Escape":
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


def search_set():
    # type: () -> None
    if not RELOAD_ON_STARTUP:
        search_window_handle = find_window_handle_by_criteria(class_name="TkTopLevel", app_name="python.exe")
        if search_window_handle:
            logger.info("found search set window, focusing")
            win32gui.SetForegroundWindow(search_window_handle)
            return
        else:
            logger.info("didn't find search set window, creating gui")

    create_gui()
