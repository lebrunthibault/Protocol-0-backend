import os.path
from os.path import dirname
from typing import Dict, List

from fastapi import FastAPI, Response, status
from fastapi.routing import APIRoute
from pydantic import BaseSettings

from lib.click import pixel_has_color
from lib.keys import send_keys
from lib.window.find_window import find_window_handle_by_enum, SearchTypeEnum, show_windows
from scripts.commands.reload_ableton import reload_ableton
from server.models import Action, Search


class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"
    api_host: str
    api_port: str

    class Config:
        env_file = "%s\\.env" % dirname(dirname(os.path.realpath(__file__)))


settings = Settings()
app = FastAPI(servers=[{"url": f"http://{settings.api_host}:{settings.api_port}", "description": "main"}],
              openapi_url=settings.openapi_url, title="Protocol0 System API")


class View():
    @app.get("/")
    def index() -> Dict:
        return {"Hello": "World"}

    @app.get("/bad_request")
    def bad_request(response: Response) -> str:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return "bad request"

    @app.get("/test/{id}")
    def test(id: int) -> Dict:
        return {"id": id}

    @app.get("/pixel_has_color/{x}/{y}/{color}")
    def pixel_has_color(request, x: int, y: int, color: str) -> bool:
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
    def arrow_up():
        send_keys("{UP}")
        return "ok"

    @app.get("/reload_ableton")
    def reload_ableton():
        reload_ableton()
        return "ok"

    @app.get("/show_windows")
    def show_windows() -> List[Dict]:
        return show_windows()

    @app.get("/search/{search}")
    def search(search: str) -> str:
        res = "You searched for : %s, last_search: %s" % (search, Search.LAST_SEARCH)
        Search.LAST_SEARCH = search
        return res

    @app.get("/action", response_model=Action)
    def action() -> Action:
        if Search.LAST_SEARCH:
            action = Action(name="SEARCH", arg=Search.LAST_SEARCH)
            Search.LAST_SEARCH = None
            return action
        else:
            return Action()


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
