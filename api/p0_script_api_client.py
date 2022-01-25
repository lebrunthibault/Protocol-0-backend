from typing import List, Dict

import mido

from loguru import logger
from p0_script_client import P0ScriptClient

from config import SystemConfig
from lib.utils import make_sysex_message_from_dict


class ScriptClientMessageSender():
    IS_LIVE = False
    DEBUG = False
    AWAITING_MESSAGES: List[Dict] = []

    @classmethod
    def _send_message_to_script(cls, data: Dict) -> None:
        from api.midi_app import get_output_port
        with mido.open_output(get_output_port(SystemConfig.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
            msg = make_sysex_message_from_dict(data=data)
            if cls.DEBUG:
                logger.info(f"sending msg to p0: {data}")
            midi_port.send(msg)

    @classmethod
    def set_live(cls):
        cls.IS_LIVE = True
        for message in cls.AWAITING_MESSAGES:
            logger.info(f"sending awaiting message {message}")
            cls._send_message_to_script(message)
        cls.AWAITING_MESSAGES = []

    @classmethod
    def send_message(cls, message):
        if not cls.IS_LIVE:
            logger.info(f"client is not live, storing message {message}")
            cls.AWAITING_MESSAGES.append(message)
            return

        cls._send_message_to_script(message)


p0_client = P0ScriptClient(message_sender=ScriptClientMessageSender())
