from lib.enum.AbstractEnum import AbstractEnum


class ColorEnum(AbstractEnum):
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @property
    def hex_value(self):
        # type: () -> str
        return self.get_value_from_mapping({
            ColorEnum.SUCCESS: "#2d985c",
            ColorEnum.WARNING: "#8c982d",
            ColorEnum.ERROR: "#ea5852"
        })
