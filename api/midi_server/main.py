import os
import signal
import sys
import time
import traceback

import mido
import requests
from loguru import logger
from mido import Message
from mido.backends.rtmidi import Input

from api.midi_server.p0_script_api_client import p0_script_client
from config import Config
from gui.celery import check_celery_worker_status, message_window, notification_window
from gui.window.message.message_factory import MessageFactory
from lib.ableton.ableton import is_ableton_up
from lib.ableton.song_state import SongState
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.timer import start_timer
from lib.utils import log_string, make_dict_from_sysex_message, make_script_command_from_sysex_message

logger = logger.opt(colors=True)
song_state = SongState()


def notify_protocol0_midi_up():
    p0_script_client.set_live()


def start_midi_server():
    system_check()
    if is_ableton_up():
        p0_script_client.set_live()

    midi_port_backend_loopback = mido.open_input(_get_input_port(Config.P0_BACKEND_LOOPBACK_NAME), autoreset=False)
    midi_port_output = mido.open_input(_get_input_port(Config.P0_OUTPUT_PORT_NAME), autoreset=False)

    logger.info(f"Midi server listening on {midi_port_backend_loopback} and {midi_port_output}. Pid {os.getpid()}")
    notification_window.delay("Midi server started")

    while True:
        _poll_midi_port(midi_port=midi_port_output)
        _poll_midi_port(midi_port=midi_port_backend_loopback)

        time.sleep(0.005)  # release cpu


def stop_midi_server():
    logger.info("stopping midi server")
    sys.exit()


def system_check():
    system_up = True

    if not check_celery_worker_status():
        start_timer(8, check_celery)

    try:
        requests.get(f"{Config.HTTP_API_URL}/")
    except requests.exceptions.ConnectionError:
        MessageFactory.show_error("HTTP server is not up")
        system_up = False

    if system_up:
        logger.info("System is up")


def check_celery():
    system_up = True
    if not check_celery_worker_status():
        MessageFactory.show_error("Celery is not up")
        system_up = False


def signal_handler(sig, frame):
    logger.warning("exiting after SIGINT")
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def _poll_midi_port(midi_port: Input):
    """ non blocking poll """
    while True:
        msg_output = midi_port.poll()
        if msg_output:
            try:
                _execute_midi_message(message=msg_output)
            except Exception as e:
                message = f"Midi server error\n\n{e}"
                message += traceback.format_exc()
                logger.error(log_string(message))
                logger.error(log_string(traceback.format_exc()))
                message_window.delay(message, NotificationEnum.ERROR.value)
        else:
            break


def _execute_midi_message(message: Message):
    # shortcut to call directly the script api
    command = make_script_command_from_sysex_message(message=message)
    if command:
        logger.info(f"received script command {command}")
        p0_script_client.dispatch(command)
        return

    payload = make_dict_from_sysex_message(message=message)
    if not payload:
        return

    logger.info(f"received midi payload {log_string(payload)}")

    # or it can exploit the routes public API by passing an operation name
    from api.midi_server.routes import Routes
    route = Routes()
    method = getattr(route, payload["method"], None)

    if method is None:
        raise Protocol0Error(f"You called an unknown backend api method: {payload} in pid {os.getpid()}")

    method(**payload["args"])


def get_output_port(port_name_prefix: str):
    return _get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_output_names())


def _get_input_port(port_name_prefix: str):
    return _get_real_midi_port_name(port_name_prefix=port_name_prefix, ports=mido.get_input_names())


def _get_real_midi_port_name(port_name_prefix: str, ports):
    # noinspection PyUnresolvedReferences
    for port_name in ports:
        if port_name_prefix in port_name:
            return port_name

    raise Exception(f"couldn't find {port_name_prefix} port")
