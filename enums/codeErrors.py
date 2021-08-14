from enum import Enum

#Clas Enum para facil manejo de excepciones
class Errors(Enum):
  INDETERMINATE_ERROR = {'code': -1, 'message': 'Indeterminate error'}
  SUCCESS = {'code': 0, 'message': 'Success'}
  INVALID_OPERATION = {'code': 1, 'message': 'Invalid operation'}
  INVALID_DATA = {'code': 2, 'message': 'Invalid data'}