from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import BaseModel

class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL:str

    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

settings=Settings()

class UserCreate(BaseModel):
    email: str
    password: str