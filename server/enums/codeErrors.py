from enum import Enum

#Clas Enum para facil manejo de excepciones
class CodeError(Enum):
  INDETERMINATE_ERROR = {'code': -1, 'message': 'Error indeterminado'}
  SUCCESS = {'code': 0, 'message': 'Operación exitosa'}
  INVALID_OPERATION = {'code': 1, 'message': 'Operación inválida'}
  INVALID_HOSPITAL = {'code': 2, 'message': 'No existe el hospital con el id proveido'}
  INVALID_BED_ID = {'code': 3, 'message': 'No existe la cama con el id proveido'}
  DELETE_OCCUPIED_BED_ERROR = {'code': 4, 'message': 'La cama a eliminar se encuentra ocupada'}
  ALREADY_OCCUPIED_BED_ERROR = {'code': 5, 'message': 'La cama ya se encuentra ocupada'}
  ALREADY_UNOCCUPIED_BED_ERROR = {'code': 6, 'message': 'La cama ya se encuentra ocupada'}
