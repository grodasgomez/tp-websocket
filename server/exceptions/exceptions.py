from enums.codeErrors import Errors

class UTIError(Exception):
    """Exception lanzada cuando hay algun error en el manejo de los mensajes.

    Attributes:
        code -- El codigo de error
        message -- Mensaje del error
    """

    def __init__(self, enum ):
        self.code = enum['code']
        self.message = enum['message']
        super().__init__(self.message)