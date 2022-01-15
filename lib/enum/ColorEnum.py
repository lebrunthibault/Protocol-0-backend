from PySimpleGUI import BLUES

from lib.enum.AbstractEnum import AbstractEnum


class ColorEnum(AbstractEnum):
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @property
    def hex_value(self):
        # type: () -> str
        return self.get_value_from_mapping({
            ColorEnum.SUCCESS: "#2d985c",
            ColorEnum.INFO: BLUES[2],
            ColorEnum.WARNING: "#8c982d",
            ColorEnum.ERROR: "#ea5852"
        })
