import threading

from PySimpleGUI import Window

from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationError(Notification):
    def __init__(self, message: str):
        super(NotificationError, self).__init__(message=message, background_color=ColorEnum.ERROR)
        self.sg_window.Title = "Error"
        self.sg_window.NoTitleBar = False
        self.sg_window.Location = (None, None)
        self.sg_window.ElementJustification = "c"

    def display(self):
        t = threading.Thread(target=self._display_in_thread, args=(self.sg_window,))
        t.setDaemon(True)
        t.start()

    def _display_in_thread(self, window: Window):
        while True:
            event, values = window.read()

            break
            # if event is None or event == "Exit" or event == sg.WIN_CLOSED:
            #     break

        window.close()
