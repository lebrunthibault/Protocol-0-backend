from api.midi_app import notify_protocol0_midi_up, stop_midi_server
from api.p0_script_api_client import protocol0
from gui.gui import show_prompt, show_message, close_current_window
from lib.ableton import reload_ableton, clear_arrangement, save_set, save_set_as_template, \
    analyze_test_audio_clip_jitter
from lib.ableton_set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.click import click, right_click, double_click, click_vertical_zone
from lib.decorators import reset_midi_client
from lib.enum.ColorEnum import ColorEnum
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from lib.window.window import focus_window
from scripts.commands.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from scripts.commands.presets import sync_presets
from scripts.commands.toggle_ableton_button import toggle_ableton_button


# noinspection PyMethodParameters
class Routes:
    def test() -> None:
        pass

    @reset_midi_client
    def ping() -> None:
        protocol0.ping()

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
        reload_ableton()

    def save_set():
        save_set()

    def save_set_as_template():
        save_set_as_template(open_pref=True)

    def clear_logs():
        protocol0.clear_logs()

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

    def search(search: str) -> None:
        protocol0.search_track(search=search)

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

    def prompt(question: str):
        show_prompt(question)

    def show_warning(message: str):
        show_message(message=message, background_color=ColorEnum.WARNING)

    def close_current_window():
        close_current_window()
