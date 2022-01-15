from gui.window.decorators.unique_window_decorator import UniqueWindowDecorator
from gui.window.prompt.prompt_error import PromptError
from gui.window.prompt.prompt_info import PromptInfo
from gui.window.window import Window
from gui.window.window_builder import WindowBuilder
from lib.enum.NotificationEnum import NotificationEnum


class PromptBuilder(WindowBuilder):
    @classmethod
    def createWindow(cls, message: str, notification_enum: NotificationEnum) -> Window:
        if notification_enum == NotificationEnum.INFO:
            prompt = PromptInfo(message=message)
        elif notification_enum == NotificationEnum.ERROR:
            prompt = PromptError(message=message)
        else:
            raise NotImplementedError

        prompt = UniqueWindowDecorator(prompt)
        return prompt
