from pydantic import EmailStr,BaseModel

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True