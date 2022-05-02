import time

import mido
from loguru import logger

from lib.midi.mido import get_output_port
from protocol0.application.command.SerializableCommand import SerializableCommand

from config import Config
from lib.enum.NotificationEnum import NotificationEnum
from lib.utils import make_sysex_message_from_command


class P0ScriptClient(object):
    def __init__(self, midi_port_name: str):
        self._is_live = False
        self._midi_port_name = midi_port_name
        self._midi_port = mido.open_output(get_output_port(self._midi_port_name), autoreset=False)

    def _send_command_to_script(self, command: SerializableCommand) -> None:
        logger.info("sending command to script!")
        logger.info(time.time())
        msg = make_sysex_message_from_command(command=command)
        self._midi_port.send(msg)
        logger.info(f"Sent script command: {command.__class__.__name__}")
        logger.info(time.time())

    def set_live(self):
        self._is_live = True

    def dispatch(self, command: SerializableCommand):
        self._send_command_to_script(command)
        from gui.celery import notification_window

        if not self._is_live:
            notification_window.delay("client is not live", NotificationEnum.WARNING.value)


p0_script_client = P0ScriptClient(Config.P0_INPUT_PORT_NAME)
p0_script_client_from_http = P0ScriptClient(Config.P0_INPUT_FROM_HTTP_PORT_NAME)
p0_script_client_from_http.set_live()
