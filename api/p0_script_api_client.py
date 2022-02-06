from typing import List

import mido

from loguru import logger
from protocol0.application.command.SerializableCommand import SerializableCommand

from config import SystemConfig
from lib.utils import make_sysex_message_from_command


class P0ScriptClient(object):
    IS_LIVE = False
    DEBUG = False
    AWAITING_COMMANDS: List[SerializableCommand] = []

    @classmethod
    def _send_command_to_script(cls, command: SerializableCommand) -> None:
        from api.midi_app import get_output_port
        with mido.open_output(get_output_port(SystemConfig.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
            if cls.DEBUG:
                logger.info(f"sending command to p0: {command}")
            msg = make_sysex_message_from_command(command=command)
            midi_port.send(msg)

    @classmethod
    def set_live(cls):
        cls.IS_LIVE = True
        for command in cls.AWAITING_COMMANDS:
            logger.info(f"sending awaiting message {command}")
            cls._send_command_to_script(command)
        cls.AWAITING_COMMANDS = []

    @classmethod
    def dispatch(cls, command: SerializableCommand):
        if not cls.IS_LIVE:
            logger.info(f"client is not live, storing message {command}")
            cls.AWAITING_COMMANDS.append(command)
            return

        cls._send_command_to_script(command)


p0_script_client = P0ScriptClient()
