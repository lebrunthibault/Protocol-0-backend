import json
import logging
import time
from json import JSONDecodeError
from typing import Dict

import mido
# noinspection PyUnresolvedReferences
from mido import Message

from lib.custom_logging import configure_logging

configure_logging(filename="midi.log")

logger = logging.getLogger(__name__)


class MidiApp():
    # port names are relative to the Protocol0 script and not this midi backend
    P0_OUTPUT_PORT_NAME = 'P0_OUT'
    P0_INPUT_PORT_NAME = 'P0_IN'

    def __init__(self):
        self._listen_to_P0_midi_messages()

    @staticmethod
    def make_message_from_string(message: str) -> Message:
        print(f"Sending string to midi output : {message}")
        b = bytearray(message.encode())
        b.insert(0, 0xF0)
        b.append(0xF7)
        return mido.Message.from_bytes(b)

    def _listen_to_P0_midi_messages(self):
        p0_port_name = None
        # noinspection PyUnresolvedReferences
        for port_name in mido.get_input_names():
            logger.debug(port_name)
            if self.P0_OUTPUT_PORT_NAME in port_name:
                p0_port_name = port_name
                break

        if p0_port_name is None:
            raise Exception(f"couldn't find {self.P0_OUTPUT_PORT_NAME} port")

        from server.routes import Routes

        # noinspection PyUnresolvedReferences
        with mido.open_input(p0_port_name, autoreset=False) as midi_port:
            start = time.time()
            logger.info(f"listening on {p0_port_name}")
            for msg in midi_port:
                if msg.is_cc(121) or msg.is_cc(123):
                    logger.debug("-")
                    continue
                bytes_msg = msg.bin()[1:-1]
                string = bytes_msg.decode("utf-8")
                logger.debug(f"Received string {string}")
                try:
                    obj = json.loads(string)
                except JSONDecodeError:
                    logger.error(f"json decode error on string : {string}, msg: {msg}")
                    continue
                method_name = obj["method"]
                method_args = obj["args"]
                method_object = getattr(Routes, method_name)
                logger.info(f"calling {method_object} with args {method_args}")
                res = method_object(**method_args)
                logger.info(f"res : {res}")

    @staticmethod
    def send_message_to_output(dict: Dict) -> None:
        p0_port_name = None
        # noinspection PyUnresolvedReferences
        for port_name in mido.get_output_names():
            logger.debug(port_name)
            if MidiApp.P0_INPUT_PORT_NAME in port_name:
                p0_port_name = port_name
                break

        if p0_port_name is None:
            raise Exception(f"couldn't find {MidiApp.P0_INPUT_PORT_NAME} port")

        # noinspection PyUnresolvedReferences
        with mido.open_output(p0_port_name, autoreset=False) as midi_port:
            logger.info(f"port open : {p0_port_name}")

            msg = MidiApp.make_message_from_string(json.dumps(dict))
            logger.info(msg)
            midi_port.send(msg)
            logger.info(f"sent msg to p0: {msg}")


if __name__ == "__main__":
    logger.info("starting app")
    MidiApp()
