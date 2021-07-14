from enum import Enum


class AbletonCommandEnum(Enum):
    KICK = "KICK"
    SNARE = "SNARE"
    CLAP = "CLAP"
    RIDE = "RIDE"
    HAT = "HAT"
    BASS = "BASS"
    # MINITAUR = "MINITAUR"
    PIANO = "PIANO"
    NEXT = "NEXT"
    HELLO = "HELLO"

    @staticmethod
    def words():
        return [enum.name.lower() for enum in AbletonCommandEnum]
