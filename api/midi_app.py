import ctypes
import json
from json import JSONDecodeError
from threading import Timer
from typing import Dict, Optional

import mido
import pyautogui
from loguru import logger

from api.p0_script_api_client import p0_script_api_client
from config import SystemConfig
from lib.process import kill_window_by_criteria
from lib.window.find_window import SearchTypeEnum

logger = logger.opt(colors=True)

DEBUG = False


class MidiCheckState:
    TIMER: Optional[Timer] = None


def ping():
    p0_script_api_client.ping()
    if MidiCheckState.TIMER:
        MidiCheckState.TIMER.cancel()
    MidiCheckState.TIMER = Timer(1.0, lambda: logger.error("Expected pong, Protocol0Midi is not loaded"))
    MidiCheckState.TIMER.start()


def pong():
    if MidiCheckState.TIMER:
        MidiCheckState.TIMER.cancel()
        MidiCheckState.TIMER = None


def send_message_to_script(data: Dict) -> None:
    # noinspection PyUnresolvedReferences
    with mido.open_output(get_output_port(SystemConfig.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
        msg = _make_sysex_message_from_dict(data=data)
        midi_port.send(msg)
        if DEBUG:
            logger.info(f"sent msg to p0: {msg}")


def start_midi_server():
    kill_window_by_criteria(name=SystemConfig.MIDI_SERVER_WINDOW_TITLE, search_type=SearchTypeEnum.WINDOW_TITLE)

    pyautogui.hotkey('win', 'up')
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.MIDI_SERVER_WINDOW_TITLE)
    from api.routes import Routes

    with mido.open_input(get_input_port(SystemConfig.P0_OUTPUT_PORT_NAME), autoreset=False) as midi_port:
        logger.info(f"Midi server listening on {midi_port}")
        for message in midi_port:
            payload = _make_dict_from_sysex_message(message=message)
            if not payload:
                continue
            method_object = getattr(Routes, payload["method"])
            logger.info(f"calling <green>{method_object.__name__}</> with args {payload['args']}")
            method_object(**payload["args"])


def get_output_port(port_name_prefix: str):
    return get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_output_names())


def get_input_port(port_name_prefix: str):
    return get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_input_names())


def get_real_midi_port_name(port_name_prefix: str, ports):
    # noinspection PyUnresolvedReferences
    for port_name in ports:
        if port_name_prefix in port_name:
            if DEBUG:
                logger.info(f"ready to open : {port_name}")
            return port_name

    raise Exception(f"couldn't find {port_name_prefix} port")


def _make_sysex_message_from_dict(data: Dict) -> mido.Message:
    assert isinstance(data, Dict)
    message = json.dumps(data)
    logger.info(f"Sending string to System midi output : <magenta>{message}</>")
    b = bytearray(message.encode())
    b.insert(0, 0xF0)
    b.append(0xF7)
    return mido.Message.from_bytes(b)


def _make_dict_from_sysex_message(message: mido.Message) -> Optional[Dict]:
    if message.is_cc(121) or message.is_cc(123):
        logger.debug("-")
        return None
    string = message.bin()[1:-1].decode("utf-8")  # type: str
    if not string.startswith("{"):
        return None
    logger.info(f"Received string <blue>{string}</>")
    try:
        return json.loads(string)
    except JSONDecodeError:
        logger.error(f"json decode error on string : {string}, message: {message}")
        return None
