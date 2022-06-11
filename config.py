import os

_ableton_version = os.environ["abletonVersion"]
_ableton_major_version = _ableton_version.split('.')[0]


class Config:
    LOGGING_DIRECTORY = os.environ.get("LOGGING_DIRECTORY")
    PROJECT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    SAMPLE_DIRECTORY = "C:\\Users\\thiba\\google_drive\\music\\software presets\\Ableton User Library\\Samples\\Imported"
    ABLETON_EXE = f"C:\\ProgramData\\Ableton\\Live {_ableton_major_version} Suite\\Program\\Ableton Live {_ableton_major_version} Suite.exe"
    ABLETON_PROCESS_NAME = f"Ableton Live {_ableton_major_version} Suite.exe"
    ABLETON_CURRENT_SET = "D:\\ableton projects\\ableton projects - " \
                          "current\\splurges\\Dark mode.als"
    ABLETON_DEFAULT_SET = "D:\\ableton projects\\ableton projects - current\\splurges\\Default.als"

    HTTP_API_URL = "http://127.0.0.1:8000"
    WS_PORT = 8080

    ABLETON_VERSION = _ableton_version
    ABLETON_WINDOW_CLASS_NAME = "Ableton Live Window Class"

    REV2_EDITOR_WINDOW_TITLE = "REV2Editor/m"
    LOG_WINDOW_TITLE = "logs terminal"
    # Midi port names are relative to the Protocol0 script and not this midi backend
    P0_OUTPUT_PORT_NAME = 'P0_OUT'
    P0_INPUT_PORT_NAME = 'P0_IN_MIDI'
    P0_INPUT_FROM_HTTP_PORT_NAME = 'P0_IN_HTTP'
    P0_BACKEND_LOOPBACK_NAME = 'P0_BACKEND_LOOPBACK'
