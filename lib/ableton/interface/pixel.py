import math
from time import sleep
from typing import Tuple

from PIL import ImageGrab

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.interface.coords import Coords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum, RGBColor
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.window.window import get_window_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


def get_color_coords(pixel_color: PixelColorEnum, box_boundary="left") -> Coords:
    assert box_boundary in ("left", "right"), "Invalid box boundary"
    screen = ImageGrab.grab()

    header_offset = 45  # skip these pixels

    pixels = list(screen.getdata())[1920 * header_offset : 1920 * 100]
    for i, coords in enumerate(pixels):
        if coords == pixel_color.rgb:
            # find the right most pixel of the selected box
            if box_boundary == "right":
                while True:
                    if coords != pixel_color.rgb:
                        break
                    i += 1
                    coords = pixels[i]
            x, y = (i % 1920, (i // 1920) + header_offset)

            if pixel_color == PixelColorEnum.TRACK_FOCUSED:
                y += 10  # drag works better here
                p0_script_client().dispatch(EmitBackendEventCommand("track_focused"))

            return x, y

    raise Protocol0Error(f"{pixel_color} not found")


def get_absolute_coords(handle: int, coords: Coords) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_coords, y_coords) = coords

    x_coords *= settings.display_resolution_factor
    y_coords *= settings.display_resolution_factor

    return (x + x_coords, y + y_coords)


def _get_pixel_color_at(coords: Coords) -> RGBColor:
    image = ImageGrab.grab()
    pixel_color = image.getpixel(coords)
    return pixel_color


def get_closest_color_at_pixel(coords: Coords) -> PixelColorEnum:
    def color_distance(c1, c2):
        # type: (RGBColor, RGBColor) -> float
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    pixel_color = _get_pixel_color_at(coords)
    return sorted(list(PixelColorEnum), key=lambda c: color_distance(c.rgb, pixel_color))[0]


@retry(10, 0)
def wait_for_pixel_color(target_color: PixelColorEnum, coords: Coords):
    if _get_pixel_color_at(coords) == target_color.rgb:
        return

    sleep(0.1)
    pixel_color = _get_pixel_color_at(coords)
    assert pixel_color == target_color.rgb, f"{pixel_color} != {target_color.rgb}"
