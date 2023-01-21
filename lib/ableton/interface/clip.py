from api.client.p0_script_api_client import p0_script_client
from api.settings import LEFT_BBOX
from lib.ableton.interface.pixel import get_coords_for_color
from lib.ableton.interface.pixel_color_enum import PixelColorEnum
from lib.ableton.interface.track import _click_context_menu
from lib.explorer import drag_file_to
from lib.mouse.mouse import keep_mouse_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def set_clip_file_path(file_path: str):
    drag_file_to(
        file_path,
        (1800, 800),
        bbox=LEFT_BBOX,
        drag_duration=0.2,
        close_window=False,
    )

    p0_script_client().dispatch(EmitBackendEventCommand("file_path_updated"))


@keep_mouse_position
def crop_clip():
    coords = get_coords_for_color(
        [PixelColorEnum.ELEMENT_FOCUSED],
        bbox=(40, 80, 1870, 750),
    )
    _click_context_menu(coords, 258)  # crop clip

    p0_script_client().dispatch(EmitBackendEventCommand("clip_cropped"))
