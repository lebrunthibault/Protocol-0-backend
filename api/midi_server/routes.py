import os
import time
from time import sleep
from typing import List, Dict

import requests
from loguru import logger

from api.midi_server.main import stop_midi_server
from api.settings import Settings
from gui.celery import select_window, notification_window
from lib.ableton.ableton import (
    reload_ableton,
    clear_arrangement,
    save_set,
    save_set_as_template,
)
from lib.ableton.analyze_clip_jitter import analyze_test_audio_clip_jitter
from lib.ableton.external_synth_track import activate_rev2_editor, post_activate_rev2_editor
from lib.ableton.interface.browser import preload_sample_category
from lib.ableton.interface.toggle_ableton_button import toggle_ableton_button
from lib.ableton.interface.track import flatten_focused_track, load_instrument_track
from lib.ableton.set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.ableton_set import AbletonSet
from lib.decorators import throttle
from lib.enum.notification_enum import NotificationEnum
from lib.keys import send_keys
from lib.mouse.mouse import click, click_vertical_zone, move_to
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import focus_window

settings = Settings()


class Routes:
    def test(self) -> None:
        pass

    def test_duplication(self) -> None:
        log_path = f"{settings.project_directory}/test_duplication.txt"
        with open(log_path, "a") as f:
            f.write(f"{time.time()} - pid: {os.getpid()}\n")
        logger.info(f"pid written to {log_path}")
        os.startfile(log_path)

    def ping(self) -> None:
        AbletonSetProfiler.end_measurement()

    def notify_set_state(self, set_data: Dict) -> None:
        # forward to http server
        requests.post(f"{settings.http_api_url}/set", data=AbletonSet(**set_data).json())

    def close_set(self, id: str) -> None:
        requests.delete(f"{settings.http_api_url}/set/{id}")

    def search(self, search: str) -> None:
        send_keys("^f")
        sleep(0.1)
        send_keys(search)

    def show_sample_category(self, category: str):
        preload_sample_category(category)

    def save_track_to_sub_tracks(self):
        # forward to http server
        requests.get(f"{settings.http_api_url}/save_track_to_sub_tracks")

    def drag_matching_track(self):
        # forward to http server
        requests.get(f"{settings.http_api_url}/drag_matching_track")

    def flatten_focused_track(self):
        flatten_focused_track()

    def move_to(self, x: int, y: int) -> None:
        move_to((x, y))

    def click(self, x: int, y: int) -> None:
        click(x=x, y=y)

    def click_vertical_zone(self, x: int, y: int) -> None:
        click_vertical_zone((x, y))

    def select_and_copy(self) -> None:
        send_keys("^a")
        send_keys("^c")

    def select_and_paste(self) -> None:
        send_keys("^a")
        send_keys("^v")

    def analyze_test_audio_clip_jitter(self, clip_path: str):
        analyze_test_audio_clip_jitter(clip_path=clip_path)

    def show_plugins(self) -> None:
        if not find_window_handle_by_enum(
            "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
        ):
            send_keys("^%p")

    def show_hide_plugins(self) -> None:
        send_keys("^%p")

    def hide_plugins(self) -> None:
        if find_window_handle_by_enum(
            "AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME
        ):
            send_keys("^%p")

    def focus_window(self, window_name: str) -> None:
        focus_window(name=window_name)

    def reload_ableton(self):
        reload_ableton()

    def save_set(self):
        save_set()

    def save_set_as_template(self):
        save_set_as_template()

    def clear_arrangement(self):
        clear_arrangement()

    def toggle_ableton_button(self, x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button((x, y), activate=activate)

    def load_instrument_track(self, instrument_name: str) -> None:
        load_instrument_track(instrument_name)

    def activate_rev2_editor(self) -> None:
        activate_rev2_editor()

    def post_activate_rev2_editor(self) -> None:
        post_activate_rev2_editor()

    def start_set_profiling(self) -> None:
        AbletonSetProfiler.start_set_profiling()

    def start_profiling_single_measurement(self) -> None:
        AbletonSetProfiler.start_profiling_single_measurement()

    def stop_midi_server(self) -> None:
        stop_midi_server()

    def show_info(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.INFO.value, centered)

    def show_success(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.SUCCESS.value, centered)

    def show_warning(self, message: str, centered: bool = False):
        notification_window.delay(message, NotificationEnum.WARNING.value, centered)

    @throttle(milliseconds=5000)
    def show_error(self, message: str):
        notification_window.delay(message, NotificationEnum.ERROR.value, centered=True)

    def select(
        self,
        question: str,
        options: List,
        vertical: bool = True,
        color: str = NotificationEnum.INFO.value,
    ):
        select_window.delay(question, options, vertical, color)
