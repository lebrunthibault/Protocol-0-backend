""" Websocket server for communication with the elgato stream deck """

import asyncio

import websockets
from loguru import logger
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

from config import Config

connected = set()


async def ws_handler(websocket):
    connected.add(websocket)

    while True:
        try:
            message = await websocket.recv()
            print("received " + message)
            # broadcast
            for connection in connected:
                await connection.send(message)
        except (ConnectionClosedOK, ConnectionClosedError):
            break

    connected.remove(websocket)


async def start_ws_server():
    logger.info("Starting websocket server")
    async with websockets.serve(ws_handler, "localhost", Config.WS_PORT):
        await asyncio.Future()  # run forever

asyncio.run(start_ws_server())
