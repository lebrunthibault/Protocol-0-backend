import signal
import sys
import time
import traceback

import mido
import requests
from loguru import logger
from mido import Message
from mido.backends.rtmidi import Input

from api.client.p0_script_api_client import p0_script_client
from config import Config
from gui.celery import check_celery_worker_status, notification_window
from gui.task_cache import TaskCache
from gui.window.notification.notification_factory import NotificationFactory
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error
from lib.midi.mido import _get_input_port
from lib.timer import start_timer
from lib.utils import (
    log_string,
    make_dict_from_sysex_message,
    make_script_command_from_sysex_message,
)

logger = logger.opt(colors=True)


def start_midi_server():
    system_check()

    midi_port_backend_loopback = mido.open_input(
        _get_input_port(Config.P0_BACKEND_LOOPBACK_NAME), autoreset=False
    )
    midi_port_output = mido.open_input(_get_input_port(Config.P0_OUTPUT_PORT_NAME), autoreset=False)

    logger.info(f"Midi server listening on {midi_port_backend_loopback} and {midi_port_output}")

    notification_window.delay("Midi server started")

    while True:
        _poll_midi_port(midi_port=midi_port_output)
        _poll_midi_port(midi_port=midi_port_backend_loopback)

        time.sleep(0.010)  # release cpu


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
        NotificationFactory.show_error("HTTP server is not up")
        system_up = False

    if system_up:
        logger.info("System is up")


def check_celery():
    TaskCache().clear()
    if not check_celery_worker_status():
        NotificationFactory.show_error("Celery is not up")


def signal_handler(sig, frame):
    logger.warning("exiting after SIGINT")
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def _poll_midi_port(midi_port: Input):
    """non blocking poll"""
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
                notification_window.delay(message, NotificationEnum.ERROR.value)
        else:
            break


def _execute_midi_message(message: Message):
    # shortcut to call directly the script api
    command = make_script_command_from_sysex_message(message=message)
    if command:
        p0_script_client().dispatch(command)
        return

    payload = make_dict_from_sysex_message(message=message)
    if not payload:
        return

    # or it can exploit the routes public API by passing an operation name
    from api.midi_server.routes import Routes

    route = Routes()
    method = getattr(route, payload["method"], None)

    if method is None:
        raise Protocol0Error(f"Unknown Route: {payload}")

    logger.info(f"GET: Route.{method.__name__}")

    method(**payload["args"])
