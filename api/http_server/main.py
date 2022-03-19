""" http / websocket gateway server to the midi server. Hit by ahk and the stream deck. """

from fastapi import FastAPI

from api.http_server.routes import router
from api.http_server.ws import ws_router
from api.midi_server.p0_backend_api_client import backend_client

app = FastAPI()
app.include_router(router)
app.include_router(ws_router)

backend_client.get_song_state()
