from typing import List, Dict

import mido
from loguru import logger
from p0_system_client import P0SystemClient

from config import SystemConfig
from lib.utils import make_sysex_message_from_dict


class SystemClientMessageSender():
    AWAITING_MESSAGES: List[Dict] = []

    @classmethod
    def send_message(cls, message):
        from api.midi_app import get_output_port
        out_port = get_output_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME)
        with mido.open_output(out_port, autoreset=False) as midi_port:
            msg = make_sysex_message_from_dict(data=message)
            midi_port.send(msg)
            logger.info(f"sent msg to p0_system via P0_SYSTEM_LOOPBACK: {message}")


system_client = P0SystemClient(message_sender=SystemClientMessageSender())
