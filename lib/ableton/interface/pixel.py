import math
from typing import Tuple

from PIL import ImageGrab
from loguru import logger

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum, RGBColor
from lib.decorators import timing
from lib.errors.Protocol0Error import Protocol0Error
from lib.window.window import get_window_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


@timing
def get_color_coords(pixel_color: PixelColorEnum) -> Coords:
    screen = ImageGrab.grab()

    header_offset = 45  # skip these pixels

    for i, coords in enumerate(list(screen.getdata())[1920 * header_offset : 1920 * 100]):
        if coords == pixel_color.rgb:
            if pixel_color == PixelColorEnum.TRACK_FOCUSED:
                p0_script_client().dispatch(EmitBackendEventCommand("track_focused"))

            return (i % 1920, (i // 1920) + header_offset)

    raise Protocol0Error(f"{pixel_color} not found")


def get_absolute_coords(handle: int, coords: Coords) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_coords, y_coords) = coords

    x_coords *= settings.display_resolution_factor
    y_coords *= settings.display_resolution_factor

    return (x + x_coords, y + y_coords)


def get_pixel_color_at(x: int, y: int) -> RGBColor:
    image = ImageGrab.grab()
    pixel_color = image.getpixel((x, y))
    logger.debug("pixel_color: %s" % PixelColorEnum.get_string_from_tuple(pixel_color))
    return pixel_color


def get_closest_color_at_pixel(x: int, y: int) -> PixelColorEnum:
    def color_distance(c1, c2):
        # type: (RGBColor, RGBColor) -> float
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    pixel_color = get_pixel_color_at(x, y)
    return sorted(list(PixelColorEnum), key=lambda c: color_distance(c.rgb, pixel_color))[0]
