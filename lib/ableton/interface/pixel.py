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
    colors: List[PixelColorEnum], box_coords: RectCoords, box_boundary="left"
) -> Coords:
    assert box_boundary in ("left", "right"), "Invalid box boundary"
    screen = ImageGrab.grab()
    colors_rgb = [c.rgb for c in colors]
    x, y, x2, y2 = box_coords

    pixels = list(screen.getdata())[1920 * y : 1920 * y2]
    for i, color in enumerate(pixels):
        x_color = i % 1920
        if not x <= x_color <= x2:
            continue
        if color in colors_rgb:
            # find the right most pixel of the selected box
            if box_boundary == "right":
                while True:
                    if color not in colors_rgb:
                        break
                    i += 1
                    color = pixels[i]
                x_color = i % 1920
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
