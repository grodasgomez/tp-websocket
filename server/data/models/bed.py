import json

class Bed:
  def __init__(self, id: str, state: bool, hospitalId: int):
    self.id = id
    self.state = state
    self.hospitalId = hospitalId
  
  def __str__(self):
    return json.dumps(self.__dict__)