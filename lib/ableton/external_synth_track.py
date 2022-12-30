from enum import Enum

from api.settings import Settings
from lib.ableton.ableton import show_plugins
from lib.ableton.interface.pixel import get_absolute_coords
from lib.mouse.mouse import click
from lib.window.find_window import find_window_handle_by_enum
from lib.window.window import focus_window

settings = Settings()


class Rev2ButtonsRelativeCoordinates(Enum):
    """These coordinates are relative to the plugin message == Mouse position relative from active_window.ahk"""

    # Relative coordinates
    ACTIVATION_MIDDLE_BUTTON = (784, 504)
    PROGRAM = (1067, 147)


def activate_rev2_editor():
    # type: () -> None
    _click_rev2_editor(Rev2ButtonsRelativeCoordinates.ACTIVATION_MIDDLE_BUTTON)


def post_activate_rev2_editor():
    # type: () -> None
    _click_rev2_editor(Rev2ButtonsRelativeCoordinates.PROGRAM)


def _click_rev2_editor(coordinates: Rev2ButtonsRelativeCoordinates):
    show_plugins()
    handle = find_window_handle_by_enum(settings.rev2_editor_window_title)
    assert handle, "Couldn't focus rev2 editor"
    focus_window(name=settings.rev2_editor_window_title)
    click(
        *get_absolute_coords(handle, coordinates.value),
        exact=True,
    )
