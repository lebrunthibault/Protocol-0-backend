from typing import List

from protocol0.application.command.ExecuteVocalCommandCommand import ExecuteVocalCommandCommand
from protocol0.application.command.PingCommand import PingCommand
from protocol0.application.command.ProcessBackendResponseCommand import ProcessBackendResponseCommand

from api.midi_app import notify_protocol0_midi_up, stop_midi_server
from api.p0_script_api_client import p0_script_client
from gui.celery import prompt_window, select_window, notification_window, kill_all_running_workers, \
    message_window
from lib.ableton import reload_ableton, clear_arrangement, save_set, save_set_as_template, \
    analyze_test_audio_clip_jitter
from lib.ableton_set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.click.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from lib.click.click import click, right_click, double_click, click_vertical_zone
from lib.click.toggle_ableton_button import toggle_ableton_button
from lib.decorators import reset_midi_client, throttle
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum
from lib.window.window import focus_window
from scripts.presets import sync_presets


class Routes:
    def test(self) -> None:
        notification_window.delay("hello boy")

    @reset_midi_client
    def ping(self) -> None:
        p0_script_client.dispatch(PingCommand())

    def notify_protocol0_midi_up(self) -> None:
        notify_protocol0_midi_up()

    def click(self, x: int, y: int) -> None:
        click(x=x, y=y)

    def click_vertical_zone(self, x: int, y: int) -> None:
        click_vertical_zone(x=x, y=y)

    def right_click(self, x: int, y: int) -> None:
        right_click(x=x, y=y)

    def double_click(self, x: int, y: int) -> None:
        double_click(x=x, y=y)

    def select_and_copy(self) -> None:
        send_keys('^a')
        send_keys('^c')

    def select_and_paste(self) -> None:
        send_keys('^a')
        send_keys('^v')

    def analyze_test_audio_clip_jitter(self, clip_path: str):
        analyze_test_audio_clip_jitter(clip_path=clip_path)

    def show_plugins(self) -> None:
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def show_hide_plugins(self) -> None:
        send_keys('^%p')

    def hide_plugins(self) -> None:
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def focus_window(self, window_name: str) -> None:
        focus_window(name=window_name)

    def reload_ableton(self):
        reload_ableton()
        AbletonSetProfiler.start_profiling_single_measurement()
        kill_all_running_workers()

    def save_set(self):
        save_set()

    def save_set_as_template(self):
        save_set_as_template(open_pref=True)

    def clear_arrangement(self):
        clear_arrangement()

    def toggle_ableton_button(self, x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    def activate_rev2_editor(self) -> None:
        activate_rev2_editor()

    def post_activate_rev2_editor(self) -> None:
        post_activate_rev2_editor()

    def sync_presets(self) -> None:
        sync_presets()

    def start_set_profiling(self) -> None:
        AbletonSetProfiler.start_set_profiling()

    def start_profiling_single_measurement(self) -> None:
        AbletonSetProfiler.start_profiling_single_measurement()

    @reset_midi_client
    def end_measurement(self) -> None:
        AbletonSetProfiler.end_measurement()

    def stop_midi_server(self) -> None:
        stop_midi_server()

    def send_backend_response(self, res) -> None:
        p0_script_client.dispatch(ProcessBackendResponseCommand(res))

    def prompt(self, question: str):
        prompt_window.delay(question)

    def show_info(self, message: str):
        notification_window.delay(message, NotificationEnum.INFO.value)

    def show_success(self, message: str):
        notification_window.delay(message, NotificationEnum.SUCCESS.value)

    def show_warning(self, message: str):
        notification_window.delay(message, NotificationEnum.WARNING.value)

    @throttle(milliseconds=5000)
    def show_error(self, message: str):
        message_window.delay(message, NotificationEnum.ERROR.value)

    def select(self, question: str, options: List, vertical: bool = True):
        select_window.delay(question, options)

    def execute_vocal_command(self, command: str):
        p0_script_client.dispatch(ExecuteVocalCommandCommand(command))
