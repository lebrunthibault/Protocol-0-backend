import math
from time import sleep
from typing import Tuple, List

from PIL import ImageGrab

from api.client.p0_script_api_client import p0_script_client
from api.settings import Settings
from lib.ableton.interface.coords import Coords, RectCoords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum, RGBColor
from lib.decorators import retry
from lib.errors.Protocol0Error import Protocol0Error
from lib.window.window import get_window_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)

settings = Settings()


def get_focused_track_coords(box_boundary="left") -> Coords:
    x, y = get_coords_for_color(
        [PixelColorEnum.TRACK_FOCUSED, PixelColorEnum.TRACK_SELECTED],
        box_coords=(40, 45, 1830, 60),
        box_boundary=box_boundary,
    )
    p0_script_client().dispatch(EmitBackendEventCommand("track_focused"))

    return x, y + 5  # drag works better here


def get_coords_for_color(
    colors: List[PixelColorEnum], box_coords: RectCoords, box_boundary="left"
) -> Coords:
    assert box_boundary in ("left", "right"), "Invalid box boundary"
    screen = ImageGrab.grab()
    colors_rgb = [c.rgb for c in colors]
    x, y, w, h = box_coords
    from loguru import logger
    logger.success(box_coords)

    pixels = list(screen.getdata())[1920 * y: 1920 * (y + h)]
    for i, color in enumerate(pixels):
        x_color = i % 1920
        if not x <= x_color <= x + w:
            continue
        if color in colors_rgb:
            # find the right most pixel of the selected box
            if box_boundary == "right":
                while True:
                    if color not in colors_rgb:
                        break
                    i += 1
                    color = pixels[i]
            return (x_color, (i // 1920) + y)

    raise Protocol0Error("color not found in screen")


def get_absolute_coords(handle: int, coords: Coords) -> Tuple[int, int]:
    (x, y, w, h) = get_window_position(handle)
    (x_coords, y_coords) = coords

    x_coords *= settings.display_resolution_factor
    y_coords *= settings.display_resolution_factor

    return (x + x_coords, y + y_coords)


def get_pixel_color_at(coords: Coords) -> RGBColor:
    image = ImageGrab.grab()
    pixel_color = image.getpixel(coords)
    return pixel_color


def get_closest_color_at_pixel(coords: Coords) -> PixelColorEnum:
    def color_distance(c1, c2):
        # type: (RGBColor, RGBColor) -> float
        (r1, g1, b1) = c1
        (r2, g2, b2) = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    pixel_color = get_pixel_color_at(coords)
    return sorted(list(PixelColorEnum), key=lambda c: color_distance(c.rgb, pixel_color))[0]


@retry(10, 0)
def wait_for_pixel_color(target_color: PixelColorEnum, coords: Coords):
    if get_pixel_color_at(coords) == target_color.rgb:
        return

    sleep(0.1)
    pixel_color = get_pixel_color_at(coords)
    assert pixel_color == target_color.rgb, f"{pixel_color} != {target_color.rgb}"
