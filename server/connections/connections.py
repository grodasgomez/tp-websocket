import asyncio
import json

import websockets
from enums.codeErrors import CodeError

#Set de todas las conexiones
CONNECTION_SET = set()

def register(websocket):
    CONNECTION_SET.add(websocket)


def unregister(websocket):
    CONNECTION_SET.remove(websocket)

async def sendAllSuccessMessage(data, operation):
    message = _getSusccesMessage(data, operation)
    for user in CONNECTION_SET:
        try:
            await user.send(message)
        except:
            unregister(user)
            
async def sendSuccessMessage(websocket, data, operation):
    message = _getSusccesMessage(data, operation)
    await websocket.send(message)

def _getSusccesMessage(data, operation):
    enumValue =  CodeError.SUCCESS.value;
    payload = {'state': enumValue['code'], 'message': enumValue['message'], 'operation': operation, 'data': data}
    return json.dumps(payload)
