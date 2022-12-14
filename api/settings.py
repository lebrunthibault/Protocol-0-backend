import os

from pydantic import BaseSettings

_ableton_version = os.environ["abletonVersion"]
_ableton_major_version = _ableton_version.split(".")[0]


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    logging_directory: str

    @property
    def log_file(self) -> str:
        return f"{self.logging_directory}\\Log.txt"

    project_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    ableton_exe = f"C:\\ProgramData\\Ableton\\Live {_ableton_major_version} Suite\\Program\\Ableton Live {_ableton_major_version} Suite.exe"
    ableton_process_name = f"Ableton Live {_ableton_major_version} Suite.exe"
    ableton_set_directory: str
    ableton_default_set = "Default.als"

    http_api_url = "http://127.0.0.1:8000"

    rev2_editor_window_title = "REV2Editor/m"
    log_window_title = "logs terminal"

    # Midi port names are relative to the Protocol0 script and not this midi backend
    p0_output_port_name = "P0_OUT"
    p0_input_port_name = "P0_IN_MIDI"
    p0_input_from_http_port_name = "P0_IN_HTTP"
    p0_backend_loopback_name = "P0_BACKEND_LOOPBACK"

    # 1 is 1080p, 2 is 4K
    display_resolution_factor = 1
