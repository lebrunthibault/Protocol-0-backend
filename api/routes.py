from api.midi_app import notify_protocol0_midi_up
from api.p0_script_api_client import protocol0
from gui.gui import show_message
from lib.ableton import reload_ableton, clear_arrangement, save_set, save_set_as_template
from lib.ableton_set_profiling.ableton_set_profiler import AbletonSetProfiler
from lib.click import click
from lib.decorators import reset_midi_client
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from lib.window.window import focus_window
from scripts.commands.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from scripts.commands.presets import sync_presets, show_protected_mode_dialog
from scripts.commands.toggle_ableton_button import toggle_ableton_button


# noinspection PyMethodParameters
class Routes:
    def test() -> None:
        protocol0.show_message("fast")

    @reset_midi_client
    def ping() -> None:
        protocol0.ping()

    def notify_protocol0_midi_up() -> None:
        notify_protocol0_midi_up()

    def click(x: int, y: int) -> None:
        click(x=x, y=y)

    def double_click(x: int, y: int) -> None:
        click(x=x, y=y, double_click=True)

    def show_plugins() -> None:
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def show_hide_plugins() -> None:
        send_keys('^%p')

    def hide_plugins() -> None:
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.WINDOW_CLASS_NAME):
            send_keys('^%p')

    def arrow_up() -> None:
        send_keys("{UP}")

    def arrow_down() -> None:
        send_keys("{DOWN}")

    def focus_window(window_name: str) -> None:
        focus_window(name=window_name)

    def reload_ableton():
        reload_ableton()

    def save_set():
        save_set()

    def save_set_as_template():
        save_set_as_template()

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

    def show_protected_mode_dialog() -> None:
        show_protected_mode_dialog()
