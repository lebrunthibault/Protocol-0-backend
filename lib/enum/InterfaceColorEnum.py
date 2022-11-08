from typing import Tuple

from lib.enum.AbstractEnum import AbstractEnum


class InterfaceColorEnum(AbstractEnum):
    @classmethod
    def get_tuple_from_string(cls, color):
        # type: (str) -> Tuple[int, int, int]
        return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))

    @classmethod
    def get_string_from_tuple(cls, color):
        # type: (Tuple[int, int, int]) -> str
        return "".join(str(hex(code).replace("0x", "").upper()) for code in color)

    def get_tuple(self):
        # type: () -> Tuple[int, int, int]
        return InterfaceColorEnum.get_tuple_from_string(self.value)

    # used when doing dynamic color detection
    ACTIVATED = "FFA608"
    NOT_SHOWN = "C3C3C3"
    DEACTIVATED = "A5A5A5"
    SEPARATOR = "4B4B4B"

    @property
    def button_activated(self) -> bool:
        return self in (InterfaceColorEnum.ACTIVATED, InterfaceColorEnum.NOT_SHOWN)

    @property
    def button_deactivated(self) -> bool:
        return self == InterfaceColorEnum.DEACTIVATED
