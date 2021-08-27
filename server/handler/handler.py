from enums.codeErrors import CodeError
from exceptions.exceptions import UTIError
from data import db
from connections import connections
from .log import Log

import logging
logging.basicConfig(level=logging.INFO)


LOG= []
async def see_state(msg, websocket):
    bedList = db.getAll()
    await connections.sendSuccessMessage(websocket, bedList, 1)


async def create_bed(msg, websocket):
    data = _validData(msg, 2, ['hospitalId'])
    bed = db.addBed(data['hospitalId'])
    _insertLog(bed.hospitalId, bed.id, 2)
    await connections.sendAllSuccessMessage(bed.__dict__, 2)


async def delete_bed(msg, websocket):
    data = _validData(msg, 3, ['bedId'])
    bedId = data['bedId']
    bed = db.deleteBed(bedId)
    _insertLog(bed.hospitalId, bedId, 3)
    await connections.sendAllSuccessMessage(bedId, 3)



async def occupy_bed(msg, websocket):
    data = _validData(msg, 4, ['bedId'])
    bedId = data['bedId']
    bed = db.occupyBed(bedId)
    _insertLog(bed.hospitalId, bedId, 4)
    await connections.sendAllSuccessMessage(bedId, 4)


async def vacate_bed(msg, websocket):
    data = _validData(msg,5, ['bedId'])
    bedId = data['bedId']
    bed = db.unoccupyBed(bedId)
    _insertLog(bed.hospitalId, bedId, 5)
    await connections.sendAllSuccessMessage(bedId, 5)

def _validData(msg, operation, fields: list):
    if (not ('data' in msg)):
        raise UTIError(CodeError.INVALID_DATA, operation)
    data = msg['data']

    for field in fields:
        if(not field in data):
            raise UTIError(CodeError.INVALID_DATA, operation)
    return data

def _insertLog(hospitalId: int, bedId: int, operation: int):
    newLog = Log(hospitalId, bedId, operation);
    logging.info('Log ->'+str(newLog))
    LOG.append(newLog)


# Creamo nuestro diccionario de las funciones que manejaran cada operacion
HANDLERS = {1: see_state, 2: create_bed,
            3: delete_bed, 4: occupy_bed, 5: vacate_bed}
