from sqlalchemy import select
from app.models.driver import Driver

def get_drivers(db):
    query=select(Driver)
    result=db.execute(query)
    return result.scalars().all()