from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connectoin import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse
from app.core.security import get_password_hash

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate,db:Session=Depends(get_db)):
    exsenting_user=db.query(User).filter(User.email==user_data.email).first()
    if exsenting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan!"
        )