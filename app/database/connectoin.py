from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

db_url=os.getenv("DATABASE_URL")

engine=create_engine(
    db_url,
    pool_size=5,
    max_overflow=2,
    
)

sessionLocal=sessionmaker(bind=engine)

def get_db():
    db=sessionLocal()

    try:
        yield db
    finally:
        db.close()