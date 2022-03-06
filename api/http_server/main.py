""" http gateway server to the midi server. Hit by ahk only. """

from fastapi import FastAPI
from protocol0.application.command.FireSceneToPositionCommand import FireSceneToPositionCommand
from protocol0.application.command.ToggleSceneLoopCommand import ToggleSceneLoopCommand

from api.p0_backend_api_client import dispatch_to_script, backend_client
from config import Config
from lib.process import execute_in_new_window

app = FastAPI()


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.get("/reload_ableton")
async def reload_ableton():
    backend_client.reload_ableton()


@app.get("/save_set_as_template")
async def save_set_as_template():
    backend_client.save_set_as_template()


@app.get("/tail_logs")
async def tail_logs():
    execute_in_new_window(f"{Config.PROJECT_ROOT}/scripts/tail_protocol0_logs.py")


@app.get("/tail_logs_raw")
async def tail_logs_raw():
    execute_in_new_window(f"{Config.PROJECT_ROOT}/scripts/tail_protocol0_logs.py", "--raw")


@app.get("/toggle_scene_loop")
async def toggle_scene_loop():
    dispatch_to_script(ToggleSceneLoopCommand())


@app.get("/fire_scene_to_position")
async def fire_scene_to_position():
    dispatch_to_script(FireSceneToPositionCommand())
