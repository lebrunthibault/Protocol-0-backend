import json
from json import JSONDecodeError
from typing import Dict

import mido
from loguru import logger

from lib.log import configure_logging

logger = logger.opt(colors=True)
configure_logging(filename="midi.log")


class MidiApp:
    IS_RUNNING = False
    DEBUG = False
    # port names are relative to the Protocol0 script and not this midi backend
    P0_OUTPUT_PORT_NAME = 'P0_OUT'
    P0_INPUT_PORT_NAME = 'P0_IN'

    def __init__(self):
        if self.IS_RUNNING:
            raise Exception("a midi app instance is already running")

        logger.info("Starting midi app")
        self.IS_RUNNING = True
        self._listen_to_p0_midi_messages()

    @staticmethod
    def _make_message_from_dict(data: Dict) -> mido.Message:
        assert isinstance(data, Dict)
        message = json.dumps(data)
        logger.info(f"Sending string to midi output : <magenta>{message}</>")
        b = bytearray(message.encode())
        b.insert(0, 0xF0)
        b.append(0xF7)
        return mido.Message.from_bytes(b)

    def _listen_to_p0_midi_messages(self):
        p0_port_name = None
        # noinspection PyUnresolvedReferences
        for port_name in mido.get_input_names():
            logger.debug(port_name)
            if MidiApp.P0_OUTPUT_PORT_NAME in port_name:
                p0_port_name = port_name
                break

        if p0_port_name is None:
            raise Exception(f"couldn't find {MidiApp.P0_OUTPUT_PORT_NAME} port")

        from api.routes import Routes

        # noinspection PyUnresolvedReferences
        with mido.open_input(p0_port_name, autoreset=False) as midi_port:
            logger.info(f"listening on {p0_port_name}")
            for msg in midi_port:
                if msg.is_cc(121) or msg.is_cc(123):
                    logger.debug("-")
                    continue
                string = msg.bin()[1:-1].decode("utf-8")  # type: str
                if not string.startswith("{"):
                    continue
                logger.info(f"Received string <blue>{string}</>")
                try:
                    obj = json.loads(string)
                except JSONDecodeError:
                    logger.error(f"json decode error on string : {string}, msg: {msg}")
                    continue
                method_object = getattr(Routes, obj["method"])
                logger.info(f"calling <green>{method_object.__name__}</> with args {obj['args']}")
                method_object(**obj["args"])

    @classmethod
    def send_message_to_script(cls, data: Dict) -> None:
        p0_port_name = None
        # noinspection PyUnresolvedReferences
        for port_name in mido.get_output_names():
            if MidiApp.P0_INPUT_PORT_NAME in port_name:
                p0_port_name = port_name
                break

        if p0_port_name is None:
            logger.error(f"couldn't find {MidiApp.P0_INPUT_PORT_NAME} port")
            return

        # noinspection PyUnresolvedReferences
        with mido.open_output(p0_port_name, autoreset=False) as midi_port:
            if cls.DEBUG:
                logger.info(f"port open : {p0_port_name}")

            msg = MidiApp._make_message_from_dict(data=data)
            midi_port.send(msg)
            if cls.DEBUG:
                logger.info(f"sent msg to p0: {msg}")


if __name__ == "__main__":
    midi_app = MidiApp()
