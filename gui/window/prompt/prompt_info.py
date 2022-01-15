from gui.window.prompt.prompt import Prompt
from lib.enum.ColorEnum import ColorEnum


class PromptInfo(Prompt):
    def __init__(self, message: str):
        super(PromptInfo, self).__init__(message=message, background_color=ColorEnum.INFO)
