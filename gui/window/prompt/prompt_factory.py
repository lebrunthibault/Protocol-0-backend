from gui.window.decorators.close_window_on_end_decorator import CloseWindowOnEndDecorator
from gui.window.decorators.notify_protocol0_decorator import NotifyProtocol0Decorator
from gui.window.prompt.prompt import Prompt
from gui.window.window import Window
from gui.window.window_factory import WindowFactory
from lib.enum.ColorEnum import ColorEnum
from lib.enum.NotificationEnum import NotificationEnum


class PromptFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO) -> Window:
        if notification_enum == NotificationEnum.INFO:
            prompt = Prompt(message=message, background_color=ColorEnum.INFO)
        elif notification_enum == NotificationEnum.ERROR:
            prompt = Prompt(message=message, background_color=ColorEnum.ERROR)
        else:
            raise NotImplementedError

        window = CloseWindowOnEndDecorator(prompt)
        window_2 = NotifyProtocol0Decorator(window)
        prompt.attach(window_2)

        return window_2
