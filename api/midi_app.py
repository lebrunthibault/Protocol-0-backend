import ctypes
import json
import time
import traceback
from json import JSONDecodeError
from pydoc import classname, locate
from threading import Timer
from typing import Dict, Optional, Callable

import mido
from loguru import logger
from mido import Message
from mido.backends.rtmidi import Input

from api.p0_script_api_client import APIMessageSender
from config import SystemConfig
from gui.window.notification.notification_factory import NotificationFactory
from lib.ableton import is_ableton_up
from lib.enum.MidiServerStateEnum import MidiServerStateEnum
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.terminal import kill_system_terminal_windows
from lib.utils import get_class_that_defined_method

logger = logger.opt(colors=True)

DEBUG = True


class MidiServerState:
    STATE = MidiServerStateEnum.UN_STARTED


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
    with mido.open_output(_get_output_port(SystemConfig.P0_INPUT_PORT_NAME), autoreset=False) as midi_port:
        msg = _make_sysex_message_from_dict(data=data)
        if DEBUG:
            logger.info(f"sending msg to p0: {data}")
        midi_port.send(msg)


def call_system_method(callable: Callable, log=True, **args) -> None:
    message = {
        "args": args
    }

    cls = get_class_that_defined_method(callable)
    if cls:
        message["class"] = classname(cls, "")
        message["method"] = callable.__name__
    else:
        message["function"] = classname(callable, "")

    out_port = _get_output_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME)
    with mido.open_output(out_port, autoreset=False) as midi_port:
        msg = _make_sysex_message_from_dict(data=message)
        midi_port.send(msg)
        logger.info(f"sent msg to p0_system via P0_SYSTEM_LOOPBACK: {message}")


def start_midi_server():
    call_system_method(stop_midi_server)  # stop already running server
    kill_system_terminal_windows()  # in case the server has errored
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.MIDI_SERVER_WINDOW_TITLE)
    if is_ableton_up():
        APIMessageSender.set_live()

    midi_port_system_loopback = mido.open_input(_get_input_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME), autoreset=False)
    midi_port_output = mido.open_input(_get_input_port(SystemConfig.P0_OUTPUT_PORT_NAME), autoreset=False)

    logger.info(f"Midi server listening on {midi_port_system_loopback} and {midi_port_output}")

    MidiServerState.STATE = MidiServerStateEnum.STARTED

    while True:
        if MidiServerState.STATE == MidiServerStateEnum.TERMINATED:
            return
        _poll_midi_port(midi_port=midi_port_output)
        _poll_midi_port(midi_port=midi_port_system_loopback)

        time.sleep(0.01)  # release cpu


def stop_midi_server():
    MidiServerState.STATE = MidiServerStateEnum.TERMINATED


def _poll_midi_port(midi_port: Input):
    """ non blocking poll """
    while True:
        msg_output = midi_port.poll()
        if msg_output:
            try:
                _execute_midi_message(message=msg_output)
            except Exception as e:
                message = f"Midi server error\n\n{e}"
                logger.error(message)
                logger.error(traceback.format_exc())
                NotificationFactory.createWindow(message=message, notification_enum=NotificationEnum.ERROR).display()
        else:
            break


def _execute_midi_message(message: Message):
    payload = _make_dict_from_sysex_message(message=message)
    if not payload:
        return

    logger.info(f"got payload {payload}")

    # call can be either explicit by giving a fqdn off a class.method or function (system loopback)
    # or it can exploit the routes public API by passing an operation name
    if payload.get("class", None):
        cls = locate(payload.get("class"))
        callable = getattr(cls, payload["method"], None)
    else:
        try:
            callable = locate(payload.get("function"))
        except AttributeError:
            from api.routes import Routes
            callable = getattr(Routes, payload["method"], None)

    if callable is None:
        raise Protocol0Error(f"You called an unknown system api method: {payload}")

    logger.info(f"received API call <green>{callable.__name__}</> with args {payload['args']}")
    callable(**payload["args"])


def _get_output_port(port_name_prefix: str):
    return _get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_output_names())


def _get_input_port(port_name_prefix: str):
    return _get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_input_names())


def _get_real_midi_port_name(port_name_prefix: str, ports):
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
