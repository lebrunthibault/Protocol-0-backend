import mido
from loguru import logger

from config import Config
from lib.midi.mido import get_output_port
from lib.utils import make_sysex_message_from_command
from protocol0.application.command.SerializableCommand import SerializableCommand


class P0ScriptClient(object):
    FROM_MIDI = None
    FROM_HTTP = None

    def __init__(self, midi_port_name: str):
        self._midi_port_name = midi_port_name
        self._midi_port = mido.open_output(get_output_port(self._midi_port_name), autoreset=False)

    def dispatch(self, command: SerializableCommand) -> None:
        from lib.ableton.ableton_set import get_focused_set

        # Pass the focused set info to the script in case of multiple sets
        focused_set = get_focused_set()
        logger.info(f"focused_set: {focused_set}")
        if focused_set is not None:
            command.set_id = focused_set.id

        msg = make_sysex_message_from_command(command=command)
        self._midi_port.send(msg)
        logger.info(f"Sent command to script: {command}")


def p0_script_client():
    if P0ScriptClient.FROM_MIDI is None:
        P0ScriptClient.FROM_MIDI = P0ScriptClient(Config.P0_INPUT_PORT_NAME)
    return P0ScriptClient.FROM_MIDI


def p0_script_client_from_http():
    if P0ScriptClient.FROM_HTTP is None:
        P0ScriptClient.FROM_HTTP = P0ScriptClient(Config.P0_INPUT_FROM_HTTP_PORT_NAME)
    return P0ScriptClient.FROM_HTTP
