import ctypes
import sys
import time
import traceback
from threading import Timer

import mido
from loguru import logger
from mido import Message
from mido.backends.rtmidi import Input

from api.p0_script_api_client import p0_script_client
from api.p0_system_api_client import system_client
from config import SystemConfig
from gui.window.notification.notification_factory import NotificationFactory
from lib.ableton import is_ableton_up
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.terminal import kill_system_terminal_windows
from lib.utils import log_string, make_dict_from_sysex_message
from message_queue.celery import notification, check_celery_worker_status, notification_error

logger = logger.opt(colors=True)


def notify_protocol0_midi_up():
    time.sleep(0.2)  # time protocol0Midi is really up for midi
    p0_script_client.set_live()


def start_midi_server():
    system_client.stop_midi_server()
    Timer(5, check_celery_is_up).start()
    kill_system_terminal_windows()  # in case the server has errored
    ctypes.windll.kernel32.SetConsoleTitleW(SystemConfig.MIDI_SERVER_WINDOW_TITLE)
    if is_ableton_up():
        p0_script_client.set_live()

    midi_port_system_loopback = mido.open_input(_get_input_port(SystemConfig.P0_SYSTEM_LOOPBACK_NAME), autoreset=False)
    midi_port_output = mido.open_input(_get_input_port(SystemConfig.P0_OUTPUT_PORT_NAME), autoreset=False)

    logger.info(f"Midi server listening on {midi_port_system_loopback} and {midi_port_output}")

    while True:
        _poll_midi_port(midi_port=midi_port_output)
        _poll_midi_port(midi_port=midi_port_system_loopback)

        time.sleep(0.01)  # release cpu


def check_celery_is_up():
    if not check_celery_worker_status():
        NotificationFactory.show_error("Celery broker is not up, closing midi server")
        system_client.stop_midi_server()
    else:
        logger.info("Celery is up")


def stop_midi_server():
    logger.info("stopping midi server")
    sys.exit()


def _poll_midi_port(midi_port: Input):
    """ non blocking poll """
    while True:
        msg_output = midi_port.poll()
        if msg_output:
            try:
                _execute_midi_message(message=msg_output)
            except Exception as e:
                message = f"Midi server error\n\n{e}"
                logger.error(log_string(message))
                logger.error(log_string(traceback.format_exc()))
                notification_error.delay(message)
        else:
            break


def _execute_midi_message(message: Message):
    payload = make_dict_from_sysex_message(message=message)
    if not payload:
        return

    logger.info(f"received midi payload {log_string(payload)}")

    # call can be either explicit by giving a fqdn off a class.method or function (system loopback)
    # or it can exploit the routes public API by passing an operation name
    from api.routes import Routes
    route = Routes()
    method = getattr(route, payload["method"], None)

    if method is None:
        raise Protocol0Error(f"You called an unknown system api method: {payload}")

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
