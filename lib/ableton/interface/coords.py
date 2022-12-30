import enum
from typing import Tuple

Coords = Tuple[int, int]


class CoordsEnum(enum.Enum):
    BROWSER_LEFT_SIZE = (18, 221)
    BROWSER_SEARCH_BOX = (86, 58)
    BROWSER_PLACE_TRACKS = (97, 284)
    BROWSER_PLACE_IMPORTED = (50, 308)
    BROWSER_FREE_TRACK_SPOT = (310, 284)

    # Relative coordinates
    REV2_ACTIVATION_MIDDLE_BUTTON = (784, 504)
    REV2_PROGRAM = (1067, 147)

    EXPLORER_FIRST_TRACK_ICON = (336, 192)
