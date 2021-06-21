import os.path
from os.path import dirname
from pathlib import Path

from fastapi import FastAPI, Response
from fastapi.routing import APIRoute
from pydantic import BaseSettings
from starlette.requests import Request

from server.custom_logging import CustomizeLogger
from server.routes import router


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
                  openapi_url=settings.openapi_url, title="Protocol0 System API",
                  description="backend API for the Protocol0 Control Surface Script. Accessible via HTTP or via MIDI. Executes on python system version without Ableton python environment limitations")
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
app.include_router(router)


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
