""" http / websocket gateway server to the midi server. Hit by ahk and the stream deck. """
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import PlainTextResponse

from api.client.p0_script_api_client import p0_script_client_from_http

load_dotenv()
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


@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(1)
    p0_script_client_from_http().dispatch(GetSetStateCommand())
