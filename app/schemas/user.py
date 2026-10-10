from pydantic import EmailStr,BaseModel

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email: str

    class Config:
        from_attributes = True