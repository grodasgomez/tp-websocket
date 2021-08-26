from typing import Dict
import uuid
from enums.codeErrors import CodeError
from exceptions.exceptions import UTIError
from .models.bed import Bed


# Diccionario en memoria que contiene todas las camas
BED_LIST: Dict[str, Bed] = {}


# Metodo que retorna todas las camas
def getAll():
    return [BED_LIST[key].__dict__ for key in BED_LIST]

# Metodo que añade una nueva cama en memoria


def addBed(hospitalId: int):
    if(hospitalId < 1 or hospitalId > 5):
        raise UTIError(CodeError.INVALID_HOSPITAL, 2)

    id = str(uuid.uuid4())
    bed = Bed(id=id, state=False, hospitalId=hospitalId)
    BED_LIST[id] = bed
    return bed

# Metodo que elimina una cama dado su id
# Retorna la cama eliminada


def deleteBed(id: str):
    existsBed(id, 3)
    isOccupied(id,3)
    return BED_LIST.pop(id)

# Marca como ocupada una cama dado su id
# Lanza un error si no existe la cama, o si ya esta ocupada


def occupyBed(id: str):
    existsBed(id, 4)
    bed = BED_LIST[id]
    if(bed.state):
        raise UTIError(CodeError.ALREADY_OCCUPIED_BED_ERROR, 4)
    bed.state = True

# Marca como desocupada una cama dado su id
# Lanza un error si no existe la cama, o si ya esta desocupada


def unoccupyBed(id: str):
    existsBed(id, 5)
    bed = BED_LIST[id]
    if(not bed.state):
        raise UTIError(CodeError.ALREADY_UNOCCUPIED_BED_ERROR, 5)
    bed.state = False

# Verifica si existe una cama, si no existe lanza un UTIError


def existsBed(id: str, operation:int):
    existsBed = id in BED_LIST
    if(not existsBed):
        raise UTIError(CodeError.INVALID_BED_ID, operation)

# Verifica si la cama esta ocupada
def isOccupied(id : str, operation:int):
    if (BED_LIST[id].state):
        raise UTIError(CodeError.DELETE_OCCUPIED_BED_ERROR, operation)
