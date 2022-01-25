import threading

from PySimpleGUI import Window
from loguru import logger

from gui.window.notification.notification import Notification
from lib.enum.ColorEnum import ColorEnum


class NotificationError(Notification):
    def __init__(self, message: str):
        super(NotificationError, self).__init__(message=message, background_color=ColorEnum.ERROR)
        self.sg_window.Title = "Error"
        self.sg_window.NoTitleBar = False
        self.sg_window.Location = (None, None)
        self.sg_window.ElementJustification = "c"
        logger.info("creating error")

    # @execute_in_thread
    def display(self):
        logger.info(f"in main: {threading.current_thread()}")
        assert threading.current_thread() is threading.main_thread()
        logger.info("display error")
        t = threading.Thread(target=self._display_in_thread, args=(self.sg_window,))
        t.setDaemon(True)
        t.start()
        t.join()
        logger.info("thread closed")

    def _display_in_thread(self, window: Window):
        logger.info(f"in thread: {threading.current_thread()}")
        logger.info("display_in_thread error")
        while True:
            event, values = window.read()

            break
            # if event is None or event == "Exit" or event == sg.WIN_CLOSED:
            #     break

        logger.info("close display_in_thread")
        window.close()
