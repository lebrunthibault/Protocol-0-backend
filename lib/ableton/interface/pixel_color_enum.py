from typing import Tuple

from lib.enum.abstract_enum import AbstractEnum

RGBColor = Tuple[int, int, int]


class PixelColorEnum(AbstractEnum):
    """used when doing dynamic color detection"""

    @classmethod
    def hex_to_rgb(cls, color: str) -> RGBColor:
        return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))

    @property
    def rgb(self) -> RGBColor:
        return PixelColorEnum.hex_to_rgb(self.value)

    BUTTON_ACTIVATED = "FFA608"
    BUTTON_ACTIVATED_2 = "FFB532"
    BUTTON_NOT_SHOWN = "C3C3C3"
    BUTTON_DEACTIVATED = "A5A5A5"

    BROWSER_BACKGROUND = "878787"
    BROWSER_SELECTED_DIM = "BFAB7A"
    BROWSER_SELECTED_DIMMER = "A8BBC4"

    ELEMENT_FOCUSED = "FF39D4"
    ELEMENT_SELECTED = "C7EDFF"
    CONTEXT_MENU_BACKGROUND = "C3C3C3"
    BLACK = "000000"

    EXPLORER_SELECTED_ENTRY = "CCE8FF"
    EXPLORER_SELECTED_ENTRY_LIGHT = "E5F3FF"

    # needed for closest color detection
    SEPARATOR = "4B4B4B"
    LEFT_SIZE = "6E6E6E"
