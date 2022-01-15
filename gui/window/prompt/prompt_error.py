from gui.window.prompt.prompt import Prompt
from lib.enum.ColorEnum import ColorEnum


class PromptError(Prompt):
    def __init__(self, message: str):
        super(PromptError, self).__init__(message=message, background_color=ColorEnum.ERROR)
