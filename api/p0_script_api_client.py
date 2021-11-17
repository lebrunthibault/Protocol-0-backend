from time import sleep
from typing import List, Dict

from p0_script_api import P0ScriptAPI
from loguru import logger


class APIMessageSender():
    IS_LIVE = False
    AWAITING_MESSAGES: List[Dict] = []

    @classmethod
    def set_live(cls):
        cls.IS_LIVE = True
        from api.midi_app import send_message_to_script

        for message in cls.AWAITING_MESSAGES:
            logger.info(f"sending awaiting message {message}")
            send_message_to_script(message)
        cls.AWAITING_MESSAGES = []

    @classmethod
    def send_message(cls, message):
        if not cls.IS_LIVE:
            logger.info(f"client is not live, storing message {message}")
            cls.AWAITING_MESSAGES.append(message)
            return

        from api.midi_app import send_message_to_script
        send_message_to_script(message)


protocol0 = P0ScriptAPI(message_sender=APIMessageSender())
