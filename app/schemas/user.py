from pydantic import BaseModel,EmailStr
from typing import Optional
import enum

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool = True

    class Config:
        from_attributes = True

class UserRole(str,enum.Enum):
    ADMIN="admin"
    DRIVER="driver"
    USER="user"

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    role:Optional[UserRole]=UserRole.USER

class UserResponseRole(BaseModel):
    id:int
    email:str
    role:str
    class Config:
        from_attributes=True
    
