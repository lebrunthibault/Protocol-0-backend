from lib.enum.AbstractEnum import AbstractEnum
from lib.enum.ColorEnum import ColorEnum


class NotificationEnum(AbstractEnum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @property
    def color(self) -> ColorEnum:
        return {
            NotificationEnum.INFO: ColorEnum.INFO,
            NotificationEnum.SUCCESS: ColorEnum.SUCCESS,
            NotificationEnum.WARNING: ColorEnum.WARNING,
            NotificationEnum.ERROR: ColorEnum.ERROR,
        }.get(self)
