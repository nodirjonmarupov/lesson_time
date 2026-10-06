from pydantic import BaseModel

class CreateDriver(BaseModel):
    name:str
    phone:str