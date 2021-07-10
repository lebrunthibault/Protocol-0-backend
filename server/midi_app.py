import json
import time
from json import JSONDecodeError
from typing import Dict

import mido
# noinspection PyUnresolvedReferences
from mido import Message

from lib.custom_logging import configure_logging

configure_logging(filename="midi.log")

from loguru import logger


class MidiApp():
    IS_RUNNING = False
    # port names are relative to the Protocol0 script and not this midi backend
    P0_OUTPUT_PORT_NAME = 'P0_OUT'
    P0_INPUT_PORT_NAME = 'P0_IN'

    def __init__(self):
        if self.IS_RUNNING:
            raise Exception("a midi app instance is already running")

        logger.info("Starting midi app")
        self.IS_RUNNING = True
        self._listen_to_P0_midi_messages()

    @staticmethod
    def _make_message_from_dict(dict: Dict) -> Message:
        assert isinstance(dict, Dict)
        message = json.dumps(dict)
        logger.info(f"Sending string to midi output : {message}")
        b = bytearray(message.encode())
        b.insert(0, 0xF0)
        b.append(0xF7)
        return mido.Message.from_bytes(b)

    def _listen_to_P0_midi_messages(self):
        p0_port_name = None
        # noinspection PyUnresolvedReferences
        for port_name in mido.get_input_names():
            logger.debug(port_name)
            if MidiApp.P0_OUTPUT_PORT_NAME in port_name:
                p0_port_name = port_name
                break

        if p0_port_name is None:
            raise Exception(f"couldn't find {MidiApp.P0_OUTPUT_PORT_NAME} port")

        from server.routes import Routes

        # noinspection PyUnresolvedReferences
        with mido.open_input(p0_port_name, autoreset=False) as midi_port:
            start = time.time()
            logger.info(f"listening on {p0_port_name}")
            for msg in midi_port:
                if msg.is_cc(121) or msg.is_cc(123):
                    logger.debug("-")
                    continue
                string = msg.bin()[1:-1].decode("utf-8")
                logger.debug(f"Received string {string}")
                try:
                    obj = json.loads(string)
                except JSONDecodeError:
                    logger.error(f"json decode error on string : {string}, msg: {msg}")
                    continue
                method_object = getattr(Routes, obj["method"])
                logger.info(f"calling {method_object} with args {obj['args']}")
                res = method_object(**obj["args"])
                logger.info(f"res : {res}")

    @staticmethod
    def send_message_to_script(dict: Dict) -> None:
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

            msg = MidiApp._make_message_from_dict(dict=dict)
            midi_port.send(msg)
            logger.info(f"sent msg to p0: {msg}")


if __name__ == "__main__":
    midi_app = MidiApp()
