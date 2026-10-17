from datetime import datetime,timedelta,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings
from sqlalchemy.orm import Session
from app.database.connectoin import get_db
from app.models.user import User


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jtw=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jtw      


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token yaroqsiz yoki mudati tugagan",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        email:str=payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except jwt.PyJWTError:
        raise credentials_exception

    user=db.query(User).filter(User.email==email).first()
    if user is None:
        raise credentials_exception

    return user


