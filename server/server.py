#!/usr/bin/env python

import asyncio
import json
import logging
import websockets
from handler.handler import HANDLERS
from enums.codeErrors import CodeError
from exceptions.exceptions import UTIError
from connections import connections


logging.basicConfig(level=logging.INFO)


# Este metodo se ejecuta cada vez que un cliente se conecta al server
async def server(websocket, path):
    connections.register(websocket)
    async for message in websocket:
        # Por cada mensaje que recibamos de este cliente en particular, se ejecutará este código
        try:
            # Validamos el mensaje
            msg = validMessage(message)
            operation = msg["operation"]
            handler = HANDLERS[operation]
            await handler(msg, websocket)
        except UTIError as e:
            await sendErrorMessage(websocket, e)


# Metodo que valida el mensaje recibido
def validMessage(message):
    msg = json.loads(message)
    logging.info(msg)
    if not "operation" in msg or not msg["operation"] in HANDLERS:
        raise UTIError(CodeError.INVALID_OPERATION)
    return msg


# Metodo que envia mensaje de error a un cliente en especifico
async def sendErrorMessage(websocket, error):
    payload = {"state": error.code, "message": error.message, "operation": error.operation}
    await websocket.send(json.dumps(payload))


# Metodos que levantan el websocket
start_server = websockets.serve(server, "localhost", 6789, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
