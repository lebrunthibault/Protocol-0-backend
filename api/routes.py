from api.midi_app import ping, pong
from api.p0_script_api_client import p0_script_api_client
from lib.ableton import reload_ableton, show_device_view
from lib.click import pixel_has_color, click
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from lib.window.window import focus_window
from scripts.commands.activate_rev2_editor import activate_rev2_editor, post_activate_rev2_editor
from scripts.commands.sync_presets import sync_presets
from scripts.commands.toggle_ableton_button import toggle_ableton_button


# noinspection PyMethodParameters
class Routes:
    def ping() -> None:
        ping()

    def pong() -> None:
        pong()

    def click(x: int, y: int) -> None:
        click(x=x, y=y)

    def double_click(x: int, y: int) -> None:
        click(x=x, y=y, double_click=True)

    def pixel_has_color(x: int, y: int, color: str) -> None:
        pixel_has_color(x=x, y=y, color=color)

    def show_device_view() -> None:
        show_device_view()

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

    def toggle_ableton_button(x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    def activate_rev2_editor() -> None:
        activate_rev2_editor()

    def post_activate_rev2_editor() -> None:
        post_activate_rev2_editor()

    def show_windows() -> None:
        show_windows()

    def search(search: str) -> None:
        p0_script_api_client.search_track(search=search)

    def sync_presets() -> None:
        sync_presets()
