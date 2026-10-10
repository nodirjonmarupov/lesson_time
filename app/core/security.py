from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings

pwd_contex=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password:str)-> str:
    return pwd_contex.hash(password)

def verify_password(plain_password:str,hashed_password:str)-> bool:
    return pwd_contex.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encode_jwt