from typing import Dict
import uuid
from enums.codeErrors import CodeError
from exceptions.exceptions import UTIError
from .models.bed import Bed


# Diccionario en memoria que contiene todas las camas
BED_LIST: Dict[str, Bed] = {}


# Metodo que retorna todas las camas
def getAll():
    return [str(BED_LIST[key]) for key in BED_LIST]

# Metodo que añade una nueva cama en memoria


def addBed(hospitalId: int):
    if(hospitalId < 1 or hospitalId > 5):
        raise UTIError(CodeError.INVALID_HOSPITAL)

    id = str(uuid.uuid4())
    bed = Bed(id=id, state=False, hospitalId=hospitalId)
    BED_LIST[id] = bed
    return bed

# Metodo que elimina una cama dado su id
# Retorna la cama eliminada


def deleteBed(id: str):
    exitsBed(id)
    return BED_LIST.pop(id)

# Marca como ocupada una cama dado su id
# Lanza un error si no existe la cama, o si ya esta ocupada


def occupateBed(id: str):
    exitsBed(id)
    bed = BED_LIST[id]
    if(bed.state):
        raise UTIError(CodeError.ALREADY_OCCUPIED_BED_ERROR)
    bed.state = True

# Marca como desocupada una cama dado su id
# Lanza un error si no existe la cama, o si ya esta desocupada


def unoccupateBed(id: str):
    exitsBed(id)
    bed = BED_LIST[id]
    if(not bed.state):
        raise UTIError(CodeError.ALREADY_UNOCCUPIED_BED_ERROR)
    bed.state = False

# Verifica si existe una cama, si no existe lanza un UTIError


def exitsBed(id: str):
    exitsBed = id in BED_LIST
    if(not exitsBed):
        raise UTIError(CodeError.INVALID_BED_ID)
