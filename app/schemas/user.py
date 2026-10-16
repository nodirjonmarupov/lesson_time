from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool = True

    class Config:
        from_attributes = True