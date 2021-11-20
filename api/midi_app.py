import ctypes
import json
import time
from json import JSONDecodeError
from threading import Timer
from typing import Dict, Optional

import mido
import pyautogui
from loguru import logger
from mido import Message

from api.p0_script_api_client import APIMessageSender
from config import SystemConfig
from lib.ableton import is_ableton_up
from lib.terminal import kill_system_terminal_windows

logger = logger.opt(colors=True)

DEBUG = True


class MidiCheckState:
    TIMER: Optional[Timer] = None


def notify_protocol0_midi_up():
    if MidiCheckState.TIMER:
        MidiCheckState.TIMER.cancel()
        MidiCheckState.TIMER = None
    time.sleep(0.2)  # time protocol0Midi is really up for midi
    APIMessageSender.set_live()


def send_message_to_script(data: Dict) -> None:
    # noinspection PyUnresolvedReferences
    with mido.open_output(get_output_port(SystemConfig.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
        msg = _make_sysex_message_from_dict(data=data)
        if DEBUG:
            logger.info(f"sending msg to p0: {data}")
        midi_port.send(msg)


def call_system_method(func: callable, **args) -> None:
    # noinspection PyUnresolvedReferences
    message = {
        "method": f"{func.__name__}",
        "args": args
    }
    out_port = get_output_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME)
    with mido.open_output(out_port, autoreset=False) as midi_port:
        msg = _make_sysex_message_from_dict(data=message)
        midi_port.send(msg)
        logger.info(f"sent msg to p0_system via P0_SYSTEM_LOOPBACK: {msg}")


def start_midi_server():
    kill_system_terminal_windows()
    pyautogui.hotkey('win', 'up')
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.MIDI_SERVER_WINDOW_TITLE)
    if is_ableton_up():
        APIMessageSender.set_live()

    midi_port_system_loopback = mido.open_input(get_input_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME), autoreset=False)
    midi_port_output = mido.open_input(get_input_port(SystemConfig.P0_OUTPUT_PORT_NAME), autoreset=False)

    logger.info(f"Midi server listening on {midi_port_system_loopback} and {midi_port_output}")

    while True:
        for msg1 in midi_port_output.iter_pending():
            _execute_midi_message(message=msg1)

        for msg in midi_port_system_loopback.iter_pending():
            _execute_midi_message(message=msg)


def _execute_midi_message(message: Message):
    from api.routes import Routes
    payload = _make_dict_from_sysex_message(message=message)
    if not payload:
        return
    logger.debug(f"got payload {payload}")
    method_object = getattr(Routes, payload["method"])
    logger.info(f"received API call <green>{method_object.__name__}</> with args {payload['args']}")
    method_object(**payload["args"])


def get_output_port(port_name_prefix: str):
    return get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_output_names())


def get_input_port(port_name_prefix: str):
    return get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_input_names())


def get_real_midi_port_name(port_name_prefix: str, ports):
    # noinspection PyUnresolvedReferences
    for port_name in ports:
        if port_name_prefix in port_name:
            return port_name

    raise Exception(f"couldn't find {port_name_prefix} port")


def _make_sysex_message_from_dict(data: Dict) -> mido.Message:
    assert isinstance(data, Dict)
    message = json.dumps(data)
    logger.debug(f"Sending string to System midi output : <magenta>{message}</>")
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
    logger.debug(f"Received string <blue>{string}</>")
    try:
        return json.loads(string)
    except JSONDecodeError:
        logger.error(f"json decode error on string : {string}, message: {message}")
        return None
