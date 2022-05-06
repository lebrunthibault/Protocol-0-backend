""" http / websocket gateway server to the midi server. Hit by ahk and the stream deck. """

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import PlainTextResponse

from api.client.p0_script_api_client import p0_script_client_from_http
from api.http_server.routes import router
from api.http_server.ws import ws_router
from protocol0.application.command.GetSongStateCommand import GetSongStateCommand

app = FastAPI(debug=True)

app.include_router(router)
app.include_router(ws_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: Exception):
    """Have verbose errors"""
    logger.info(str(exc))
    return PlainTextResponse(str(exc), status_code=400)


p0_script_client_from_http().dispatch(GetSongStateCommand())
