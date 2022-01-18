from gui.window.decorators.close_window_on_end_decorator import CloseWindowOnEndDecorator
from gui.window.decorators.notify_protocol0_decorator import NotifyProtocol0Decorator
from gui.window.decorators.unique_window_decorator import UniqueWindowDecorator
from gui.window.prompt.prompt_error import PromptError
from gui.window.prompt.prompt_info import PromptInfo
from gui.window.window import Window
from gui.window.window_factory import WindowFactory
from lib.enum.NotificationEnum import NotificationEnum


class PromptFactory(WindowFactory):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum = NotificationEnum.INFO) -> Window:
        if notification_enum == NotificationEnum.INFO:
            prompt = PromptInfo(message=message)
        elif notification_enum == NotificationEnum.ERROR:
            prompt = PromptError(message=message)
        else:
            raise NotImplementedError

        window = UniqueWindowDecorator(prompt)
        window = CloseWindowOnEndDecorator(window)
        window = NotifyProtocol0Decorator(window)
        prompt.attach(window)

        return window
