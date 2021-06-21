from typing import Dict, List

from fastapi import APIRouter
from fastapi import Response, status

from lib.click import pixel_has_color, click
from lib.keys import send_keys
from lib.window.ableton import show_device_view
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from lib.window.window import focus_window
from scripts.commands.activate_rev2_editor import activate_rev2_editor
from scripts.commands.reload_ableton import reload_ableton
from scripts.commands.sync_presets import sync_presets
from scripts.commands.toggle_ableton_button import toggle_ableton_button
from server.midi_app import MidiApp
from server.models import Search

router = APIRouter()


class Routes():
    @router.get("/")
    def index() -> Dict:
        return {"Hello": "World"}

    @router.get("/health")
    def health() -> Dict:
        return {"status": "up"}

    @router.get("/bad_request")
    def bad_request(response: Response) -> str:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "bad request"

    @router.get("/click/{x}/{y}")
    def click(x: int, y: int) -> None:
        click(x=x, y=y)

    @router.get("/double_click/{x}/{y}")
    def double_click(x: int, y: int) -> None:
        click(x=x, y=y, double_click=True)

    @router.get("/pixel_has_color/{x}/{y}/{color}", response_model=bool)
    def pixel_has_color(x: int, y: int, color: str) -> bool:
        return pixel_has_color(x=x, y=y, color=color)

    @router.get("/show_device_view")
    def show_device_view() -> None:
        show_device_view()

    @router.get("/show_plugins")
    def show_plugins() -> None:
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')

    @router.get("/show_hide_plugins")
    def show_hide_plugins() -> None:
        send_keys('^%p')

    @router.get("/hide_plugins")
    def hide_plugins() -> None:
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')

    @router.get("/arrow_up")
    def arrow_up() -> None:
        send_keys("{UP}")

    @router.get("/arrow_down")
    def arrow_down() -> None:
        send_keys("{DOWN}")

    @router.get("/focus_window/{window_name}")
    def focus_window(window_name: str) -> bool:
        return focus_window(name=window_name)

    @router.get("/reload_ableton")
    def reload_ableton():
        reload_ableton()

    @router.get("/toggle_ableton_button/{x}/{y}/{activate}")
    def toggle_ableton_button(x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    @router.get("/activate_rev2_editor")
    def activate_rev2_editor() -> None:
        activate_rev2_editor()

    @router.get("/show_windows")
    def show_windows() -> List[Dict]:
        return show_windows()

    @router.get("/search/{search}")
    def search(search: str) -> str:
        MidiApp.send_message_to_output({"enum": "SEARCH_TRACK", "arg": search})
        Search.LAST_SEARCH = search
        return f"You searched for : {search}"
        return res

    @router.get("/sync_presets", response_model=str)
    def sync_presets() -> str:
        return sync_presets()
