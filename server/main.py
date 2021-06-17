import os.path
from os.path import dirname
from pathlib import Path
from typing import Dict, List

from a_protocol_0.enums.ServerActionEnum import ServerActionEnum
from fastapi import FastAPI, Response, status
from fastapi import WebSocket
from fastapi.routing import APIRoute
from lib.click import pixel_has_color, click
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows, is_plugin_window_visible
from lib.window.window import focus_window
from loguru import logger
from pydantic import BaseSettings
from scripts.commands.activate_rev2_editor import activate_rev2_editor
from scripts.commands.reload_ableton import reload_ableton
from scripts.commands.sync_presets import sync_presets
from scripts.commands.toggle_ableton_button import toggle_ableton_button
from server.custom_logging import CustomizeLogger
from server.models import Action, Search
from starlette.requests import Request


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"
    api_host: str
    api_port: str

    class Config:
        env_file = "%s\\.env" % dirname(dirname(os.path.realpath(__file__)))


settings = Settings()

config_path = Path(__file__).with_name("logging_config.json")


def create_app() -> FastAPI:
    app = FastAPI(servers=[{"url": f"http://{settings.api_host}:{settings.api_port}", "description": "main"}],
                  openapi_url=settings.openapi_url, title="Protocol0 System API")
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            logger.exception("Stack trace", stdout_only=True)
            return Response(f"Internal server error: {e}", status_code=500)

    app.middleware('http')(catch_exceptions_middleware)

    return app


app = create_app()


class Routes():
    @app.get("/")
    def index() -> Dict:
        logger.info("logging from the root logger")
        return {"Hello": "World"}

    @app.get("/health")
    def health() -> Dict:
        return {"status": "up"}

    @app.get("/bad_request")
    def bad_request(response: Response) -> str:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "bad request"

    @app.get("/click/{x}/{y}")
    def click(x: int, y: int) -> None:
        click(x=x, y=y)

    @app.get("/double_click/{x}/{y}")
    def double_click(x: int, y: int) -> None:
        click(x=x, y=y, double_click=True)

    @app.get("/pixel_has_color/{x}/{y}/{color}", response_model=bool)
    def pixel_has_color(x: int, y: int, color: str) -> bool:
        return pixel_has_color(x=x, y=y, color=color)

    @app.get("/show_plugins")
    def show_plugins() -> None:
        if not find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')

    @app.get("/show_hide_plugins")
    def show_hide_plugins() -> None:
        send_keys('^%p')

    @app.get("/hide_plugins")
    def hide_plugins() -> None:
        if find_window_handle_by_enum("AbletonVstPlugClass", search_type=SearchTypeEnum.CLASS):
            send_keys('^%p')

    @app.get("/arrow_up")
    def arrow_up() -> None:
        send_keys("{UP}")

    @app.get("/arrow_down")
    def arrow_down() -> None:
        send_keys("{DOWN}")

    @app.get("/focus_window/{window_name}")
    def focus_window(window_name: str) -> bool:
        return focus_window(name=window_name)

    @app.get("/is_plugin_window_visible/{name}", response_model=bool)
    def is_plugin_window_visible(name: str) -> bool:
        return is_plugin_window_visible(name=name)

    @app.get("/reload_ableton")
    def reload_ableton():
        reload_ableton()

    @app.get("/toggle_ableton_button/{x}/{y}/{activate}")
    def toggle_ableton_button(x: int, y: int, activate: bool = False) -> None:
        toggle_ableton_button(x=x, y=y, activate=activate)

    @app.get("/activate_rev2_editor")
    def activate_rev2_editor() -> None:
        activate_rev2_editor()

    @app.get("/show_windows")
    def show_windows() -> List[Dict]:
        return show_windows()

    @app.get("/search/{search}")
    def search(search: str) -> str:
        res = "You searched for : %s, last_search: %s" % (search, Search.LAST_SEARCH)
        Search.LAST_SEARCH = search
        return res

    @app.get("/sync_presets", response_model=str)
    def sync_presets() -> str:
        return sync_presets()

    @app.get("/action", response_model=Action)
    def action() -> Action:
        if Search.LAST_SEARCH:
            action = Action(enum=ServerActionEnum.SEARCH_TRACK, arg=Search.LAST_SEARCH)
            Search.LAST_SEARCH = None
            return action
        else:
            return Action()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

        # await asyncio.sleep(1)
        # payload = {"time": time.time()}
        # await websocket.send_json(payload)


# should be after the routes are defined
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
