from enums.codeErrors import CodeError

class UTIError(Exception):
    """Exception lanzada cuando hay algun error en el manejo de los mensajes.

    Attributes:
        code -- El codigo de error
        message -- Mensaje del error
    """

    def __init__(self, enum: CodeError, operation:int = None):
        value = enum.value;
        self.code = value['code']
        self.operation = operation
        self.message = value['message']
        super().__init__(self.message)