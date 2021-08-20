#!/usr/bin/env python

import asyncio
import json
import logging
import websockets
from handler.handler import HANDLERS
from enums.codeErrors import Errors
from exceptions.exceptions import UTIError


##CODIGO DE EJEMPLO
logging.basicConfig(level=logging.INFO)

STATE = {"value": 0}

USERS = set()

def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

##FIN DEL CODIGO DE EJEMPLO





#Este metodo se ejecuta cada vez que un cliente se conecta al server
async def server(websocket, path):
    await register(websocket)
    await websocket.send(state_event())
    async for message in websocket:
        #Por cada mensaje que recibamos de este cliente en particular, se ejecutará este código
        try:
            # Validamos el mensaje
            msg = validMessage(message)
            operation = msg['operation']
            data = msg['data']
            handler = HANDLERS[operation]
            handler(data)
        except UTIError as e:
            await sendErrorMessage(websocket, e, -1)

    

#Metodo que valida el mensaje recibido
def validMessage(message):
    msg = json.loads(message)
    logging.info(msg)
    if (not ('operation' in msg) or not(msg['operation'] in HANDLERS)):
        raise UTIError(Errors.INVALID_OPERATION.value)
    if (not ('data' in msg)):
        raise UTIError(Errors.INVALID_DATA.value)
    return msg

#Metodo que envia mensaje de error a un cliente en especifico
async def sendErrorMessage(websocket, error, operation):
    payload = {'state': error.code, 'message': error.message, 'operation': operation}
    await websocket.send(json.dumps(payload))


#Metodos que levantan el websocket
start_server = websockets.serve(server, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
