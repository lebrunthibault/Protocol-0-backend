from typing import Optional

from sr.audio.recording import Recording
from sr.enums.ableton_command_enum import AbletonCommandEnum


class RecognizerResult:
    def __init__(self, recording: Recording):
        self.recording = recording
        self.word: Optional[str] = None
        self.word_enum: Optional[AbletonCommandEnum] = None

    def __str__(self):
        # return f"{self.word} -> {self.word_enum.name if self.word_enum else ''}"
        return self.word_enum.name if self.word_enum else self.word
