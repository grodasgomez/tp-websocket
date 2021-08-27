import json
from datetime import datetime

class Log:
    def __init__(self,hospitalId, bedId, operation):
        self.hospitalId = hospitalId;
        self.bedId = bedId;
        self.operation = operation;
        self.dateTime = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")

    def __str__(self):
        return json.dumps(self.__dict__)

    