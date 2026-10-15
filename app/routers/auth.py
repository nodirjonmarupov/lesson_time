from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connectoin import get_db
from app.models.user import User
from app.core.security import verify_password
from fastapi.security import OAuth2PasswordRequestForm
# (Token yaratish uchun kerak bo'ladigan funksiyalarni keyingi qadamda yozamiz, hozircha oddiy logikasini ko'ramiz)
router = APIRouter(prefix="/auth", tags=["Auth"])

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
    
    # 3. Agar hammasi to'g'ri bo'lsa (Hozircha oddiy xabar qaytaramiz)
    return {"message": "Muvaffaqiyatli kirdingiz!", "user_id": user.id}