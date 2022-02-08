from typing import List

from protocol0.domain.command.ClearLogsCommand import ClearLogsCommand
from protocol0.domain.command.ExecuteVocalCommandCommand import ExecuteVocalCommandCommand
from protocol0.domain.command.PingCommand import PingCommand
from protocol0.domain.command.ProcessSystemResponseCommand import ProcessSystemResponseCommand

from api.midi_app import notify_protocol0_midi_up, stop_midi_server
from api.p0_script_api_client import p0_script_client
from lib.ableton import reload_ableton, clear_arrangement, save_set, save_set_as_template, \
    analyze_test_audio_clip_jitter
from lib.ableton_set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.click import click, right_click, double_click, click_vertical_zone
from lib.decorators import reset_midi_client
from lib.enum.NotificationEnum import NotificationEnum
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from lib.window.window import focus_window
from message_queue.celery import prompt, select, notification
from scripts.commands.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from scripts.commands.presets import sync_presets
from scripts.commands.toggle_ableton_button import toggle_ableton_button


# noinspection PyMethodParameters
class Routes:
    def test() -> None:
        p0_script_client.dispatch(ClearLogsCommand())

    @reset_midi_client
    def ping() -> None:
        p0_script_client.dispatch(PingCommand())

    def notify_protocol0_midi_up() -> None:
        notify_protocol0_midi_up()

    def click(x: int, y: int) -> None:
        click(x=x, y=y)

    def click_vertical_zone(x: int, y: int) -> None:
        click_vertical_zone(x=x, y=y)

    def right_click(x: int, y: int) -> None:
        right_click(x=x, y=y)

    def double_click(x: int, y: int) -> None:
        double_click(x=x, y=y)

    def analyze_test_audio_clip_jitter(clip_path: str):
        analyze_test_audio_clip_jitter(clip_path=clip_path)

    def show_plugins() -> None:
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def show_hide_plugins() -> None:
        send_keys('^%p')

    def hide_plugins() -> None:
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def focus_window(window_name: str) -> None:
        focus_window(name=window_name)

    def reload_ableton():
        AbletonSetProfiler.start_profiling_single_measurement()
        reload_ableton()

    def save_set():
        save_set()

    def save_set_as_template():
        save_set_as_template(open_pref=True)

    def clear_logs():
        p0_script_client.dispatch(ClearLogsCommand())

    def clear_arrangement():
        clear_arrangement()

    def toggle_ableton_button(x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    def activate_rev2_editor() -> None:
        activate_rev2_editor()

    def post_activate_rev2_editor() -> None:
        post_activate_rev2_editor()

    def show_windows() -> None:
        show_windows()

    def sync_presets() -> None:
        sync_presets()

    def start_set_profiling() -> None:
        AbletonSetProfiler.start_set_profiling()

    def start_profiling_single_measurement() -> None:
        AbletonSetProfiler.start_profiling_single_measurement()

    @reset_midi_client
    def end_measurement() -> None:
        AbletonSetProfiler.end_measurement()

    def stop_midi_server() -> None:
        stop_midi_server()

    def send_system_response(res) -> None:
        p0_script_client.dispatch(ProcessSystemResponseCommand(res))

    def prompt(question: str):
        prompt.delay(question)

    def select(question: str, options: List[str], vertical=True):
        select.delay(question, options)

    def show_warning(message: str):
        notification.delay(message, NotificationEnum.WARNING.value)

    def show_error(message: str):
        notification.delay(message, NotificationEnum.ERROR.value)

    def execute_vocal_command(command: str):
        p0_script_client.dispatch(ExecuteVocalCommandCommand(command))
