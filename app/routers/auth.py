from fastapi import APIRouter, Depends, HTTPException, status
from app.database.connectoin import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse
from app.core.security import get_password_hash
from app.schemas.user import UserLogin, Token
from app.core.security import verify_password, create_access_token

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate,db:Session=Depends(get_db)):
    exsenting_user=db.query(User).filter(User.email==user_data.email).first()
    if exsenting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan!"
        )

    hashed_pwd=get_password_hash(user_data.password)

    new_user=User(
        email=user_data.email,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login",response_model=Token)
def login_user(user_data:UserLogin,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="email yoki parol notog'ri!",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="email yoki parol notog'ri!",
                    headers={"WWW-Authenticate": "Bearer"}
                )
    access_token=create_access_token({"sub":user.email})
    return {"access_token":access_token,"token_type":"bearer"}

    