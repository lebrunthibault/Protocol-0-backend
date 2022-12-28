from typing import cast

from lib.enum.abstract_enum import AbstractEnum
from lib.enum.color_enum import ColorEnum


class NotificationEnum(AbstractEnum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"

    @property
    def color(self) -> ColorEnum:
        return cast(
            ColorEnum,
            {
                NotificationEnum.INFO: ColorEnum.INFO,
                NotificationEnum.SUCCESS: ColorEnum.SUCCESS,
                NotificationEnum.WARNING: ColorEnum.WARNING,
                NotificationEnum.ERROR: ColorEnum.ERROR,
            }.get(self),
        )
