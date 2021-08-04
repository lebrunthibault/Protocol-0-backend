from dataclasses import dataclass
from typing import Optional

from sr.enums.ableton_command_enum import AbletonCommandEnum


@dataclass
class RecognizerResult:
    word: str
    word_enum: Optional[AbletonCommandEnum]
    #
    # def __init__(self, word: str):
    #     self.word = word
    #     self.word_enum: Optional[AbletonCommandEnum] = None
    #
    # def __str__(self):
    #     return self.word_enum.name if self.word_enum else self.word
