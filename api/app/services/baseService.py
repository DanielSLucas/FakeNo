import json

class BaseService:
  name = ''
  result = None

  def __init__(self, name) -> None:
    self.name = name

  def execute(self):
    raise Exception("Execute method not implemented")
  
  def to_json(self):
    return json.dumps({ "name": self.name, "result": self.result })