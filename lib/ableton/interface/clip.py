from api.client.p0_script_api_client import p0_script_client
from lib.explorer import drag_file_to
from lib.mouse.mouse import keep_mouse_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def set_clip_file_path(file_path: str):
    drag_file_to(file_path, (1860, 800), close_window=False)
    p0_script_client().dispatch(EmitBackendEventCommand("file_path_updated"))
