from typing import List

import mido
from loguru import logger
from protocol0.application.command.SerializableCommand import SerializableCommand

from config import Config
from lib.utils import make_sysex_message_from_command


class P0ScriptClient(object):
    DEBUG = False

    def __init__(self):
        self._is_live = False
        self._awaiting_commands: List[SerializableCommand] = []

    def _send_command_to_script(self, command: SerializableCommand) -> None:
        from api.midi_app import get_output_port
        with mido.open_output(get_output_port(Config.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
            if self.DEBUG:
                logger.info(f"sending command to p0: {command}")
            msg = make_sysex_message_from_command(command=command)
            midi_port.send(msg)

    def set_live(self):
        self._is_live = True
        for command in self._awaiting_commands:
            self._send_command_to_script(command)
        self._awaiting_commands = []

    def dispatch(self, command: SerializableCommand):
        if not self._is_live:
            logger.info(f"client is not live, storing message {command}")
            self._awaiting_commands.append(command)
            return

        self._send_command_to_script(command)


p0_script_client = P0ScriptClient()
