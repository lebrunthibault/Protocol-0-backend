import mido
from loguru import logger
from protocol0.application.command.SerializableCommand import SerializableCommand

from config import Config
from gui.celery import notification_window
from lib.enum.NotificationEnum import NotificationEnum
from lib.utils import make_sysex_message_from_command


class P0ScriptClient(object):
    DEBUG = False

    def __init__(self):
        self._is_live = False

    def _send_command_to_script(self, command: SerializableCommand) -> None:
        from api.midi_server.main import get_output_port
        with mido.open_output(get_output_port(Config.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
            msg = make_sysex_message_from_command(command=command)
            midi_port.send(msg)
            logger.info(f"Sent script command: {command.__class__.__name__}")

    def set_live(self):
        self._is_live = True

    def dispatch(self, command: SerializableCommand):
        if not self._is_live:
            notification_window.delay("client is not live", NotificationEnum.WARNING.value)

        self._send_command_to_script(command)


p0_script_client = P0ScriptClient()