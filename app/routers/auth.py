from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connectoin import get_db
from app.models.user import User
from app.core.security import verify_password,get_password_hash
from fastapi.security import OAuth2PasswordRequestForm
from app.core.jtw import get_current_user
from app.core.config import UserCreate
from app.core.jtw import create_access_token
from app.schemas.user import UserCreate,UserRole,UserResponseRole
# (Token yaratish uchun kerak bo'ladigan funksiyalarni keyingi qadamda yozamiz, hozircha oddiy logikasini ko'ramiz)
router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    # 1. Bazadan foydalanuvchini email bo'yicha qidirib topamiz
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Agar foydalanuvchi topilmasa yoki parol xato bo'lsa
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol xato!",
        )
    access_token = create_access_token(data={"sub": user.email})
    
    # 3. Agar hammasi to'g'ri bo'lsa (Hozircha oddiy xabar qaytaramiz)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_user_me(
    current_users_email: str = Depends(get_current_user),
    db: Session = Depends(get_db)

):
    user=db.query(User).filter(User.email==current_users_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi!"
        )
    return user


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Bu email oldindan bormi yo'qligini tekshiramiz
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan!"
        )
    
    # 2. Parolni xashlaymiz (shifrlaymiz)
    hashed_password = get_password_hash(user_data.password)
    
    # 3. Yangi foydalanuvchini yaratamiz
    new_user = User(email=user_data.email, 
                    hashed_password=hashed_password,
                    role=user_data.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi!", "email": new_user.email}