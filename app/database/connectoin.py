from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="postgresql://my_database:2002@localhost:5432/fastapi_db"
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