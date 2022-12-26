""" http / websocket gateway server to the midi server. Hit by ahk and the stream deck. """
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# needed when calling protocol0 Config
from lib.enum.NotificationEnum import NotificationEnum
from lib.errors.Protocol0Error import Protocol0Error

load_dotenv()

from gui.celery import notification_window
from api.client.p0_script_api_client import p0_script_client_from_http
from api.http_server.routes import router  # noqa
from api.http_server.ws import ws_router  # noqa
from protocol0.application.command.GetSetStateCommand import GetSetStateCommand  # noqa

app = FastAPI(debug=True)

app.include_router(router)
app.include_router(ws_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: Exception):
    """Have verbose errors"""
    logger.info(str(exc))
    return PlainTextResponse(str(exc), status_code=400)


@app.middleware("http")
async def _catch_protocol0_errors(request: Request, call_next):
    try:
        return await call_next(request)
    except Protocol0Error as e:
        notification_window.delay(
            str(e), notification_enum=NotificationEnum.WARNING.value, centered=True
        )
        return PlainTextResponse(str(e), status_code=400)


async def _get_state():
    """Delaying so the http and midi servers are up to receive set data"""
    await asyncio.sleep(3)
    p0_script_client_from_http().dispatch(GetSetStateCommand())


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(_get_state())
