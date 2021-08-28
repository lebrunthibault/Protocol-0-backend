from time import sleep

import PySimpleGUI as sg
import pyautogui
from PySimpleGUI import POPUP_BUTTONS_NO_BUTTONS
from loguru import logger

from sr.recognizer.recognizer_result import RecognizerResult

logger = logger.opt(colors=True)


class SpeechGui(object):
    # def __init__(self, recognizer_result: RecognizerResult):
    #     super().__init__()
    #     self.window: Optional[sg.Window] = None
    #     # threading.Thread(target=partial(self.create_window, message), daemon=True).start()
    #     self.create_window(message=message)
    #     # balloon_tip(msg=message)

    # def handle_string_message(self, message):
    #     # self.window.TKroot.focus_force()  # force this window to have focus
    #     self.window["logs"].update(str(message))

    @staticmethod
    def display_recognizer_result(recognizer_result: RecognizerResult):
        message = str(recognizer_result)
        sg.popup(message,
                 auto_close=True,
                 auto_close_duration=1,
                 no_titlebar=True,
                 location=(pyautogui.size()[0] - (80 + 6 * len(message)), 10),
                 background_color=recognizer_result.display_color,
                 keep_on_top=True,
                 # non_blocking=True,
                 modal=False,
                 button_type=POPUP_BUTTONS_NO_BUTTONS,
                 )
        return

        layout = [[sg.Text(str(recognizer_result), key="logs", background_color=background_color)]]
        # layout = [[sg.Text(message, key="logs", background_color=background_color, size=(200, 30), pad=(10, 8))],
        #           [sg.Quit(size=(30, 30))]]

        window = sg.Window(
            "sr log",
            layout,
            no_titlebar=True,
            background_color=background_color,
            location=(pyautogui.size()[0] - 270, 20),
            finalize=True,
            # auto_size_text=False,
            alpha_channel=.7,
            # size=(160, 40),
        )
        window.bring_to_front()

        sleep(1)
        # while True:  # Event Loop
        #     # Please try and use as high of a timeout value as you can
        #     event, values = self.window.read(timeout=1000)
        #
        #     # if user closed the window using X or clicked Quit button
        #     if event in (sg.WIN_CLOSED, "Quit"):
        #         break

        logger.info("closing GUI window")
        window.close()
