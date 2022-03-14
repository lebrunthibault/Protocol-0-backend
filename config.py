import os

_ableton_version = os.environ["abletonVersion"]
_ableton_major_version = _ableton_version.split('.')[0]


class Config:
    LOGGING_DIRECTORY = os.environ.get("LOGGING_DIRECTORY")
    PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

    HTTP_API_URL = "http://127.0.0.1:8000"
    WS_PORT = 8080

    ABLETON_VERSION = _ableton_version
    ABLETON_WINDOW_CLASS_NAME = "Ableton Live Window Class"
    ABLETON_EXE = f"Ableton Live {_ableton_major_version} Suite.exe"

    REV2_EDITOR_WINDOW_TITLE = "REV2Editor/midi"
    LOG_WINDOW_TITLE = "logs terminal"
    # Midi port names are relative to the Protocol0 script and not this midi backend
    P0_OUTPUT_PORT_NAME = 'P0_OUT'
    P0_INPUT_PORT_NAME = 'P0_IN'
    P0_BACKEND_LOOPBACK_NAME = 'P0_BACKEND_LOOPBACK'
