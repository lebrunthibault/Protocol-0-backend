from api.client.p0_script_api_client import p0_script_client
from api.settings import RIGHT_BBOX
from lib.explorer import drag_file_to
from lib.mouse.mouse import keep_mouse_position
from protocol0.application.command.EmitBackendEventCommand import (
    EmitBackendEventCommand,
)


@keep_mouse_position
def load_sample_in_simpler(sample_path: str):
    drag_file_to(sample_path, (55, 800), bbox=RIGHT_BBOX)
    p0_script_client().dispatch(EmitBackendEventCommand("sample_loaded"))
