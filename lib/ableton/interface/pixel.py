import math
from typing import Tuple, List

from PIL import ImageGrab

from api.settings import Settings
from lib.ableton.interface.coords import Coords, RectCoords
from lib.ableton.interface.pixel_color_enum import PixelColorEnum, RGBColor
from lib.errors.Protocol0Error import Protocol0Error
from lib.window.window import get_window_position

settings = Settings()


def get_coords_for_color(
    colors: List[PixelColorEnum], bbox: RectCoords = None, box_boundary="left"
) -> Coords:
    assert box_boundary in ("left", "right"), "Invalid box boundary"
    screen = ImageGrab.grab(bbox=bbox)

    colors_rgb = [c.rgb for c in colors]
    x1, y1, x2, _ = bbox
    width = x2 - x1

    pixels = list(enumerate(screen.getdata()))
    for i, color in pixels[::20]:
        if color not in colors_rgb:
            continue

        if box_boundary == "right":
            while True:
                if color not in colors_rgb:
                    break
                i += 1
                color = pixels[i]

        return ((i % width) + x1, (i // width) + y1)

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
