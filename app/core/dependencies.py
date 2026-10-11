from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# O'zingizning loyihangizdagi fayl yo'llariga qarab bularni moslaysiz:
from app.database.connectoin import get_db        # Bazaga ulanish sessiyasi
from app.models.user import User                  # SQLAlchemy User modeli
from app.core.security import verify_access_token # Oldin yozgan token tekshiruvchi funksiyamiz
from app.schemas.user import UserResponse         # Pydantic javob qolipi (schema)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# 1. OAuth2 scheme: Token qayerdan kelishini va Swagger uchun login URL manzilini ko'rsatamiz
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 2. Dependency: Tokenni tekshirib, bazadan foydalanuvchini topib beruvchi qo'riqchi funksiya
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati o'tgan!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Tokondan emailni sug'urib olamiz (verify_access_token yordamida)
    email = verify_access_token(token, credentials_exception)
    
    # Bazadan shu emailli foydalanuvchini qidiramiz
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user


# 3. Endpoint: Faqat to'g'ri token bilan kirganlar o'qiy oladigan himoyalangan yo'l
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Tizimga kirgan foydalanuvchining o'z ma'lumotlarini qaytaruvchi endpoint.
    """
    return current_user