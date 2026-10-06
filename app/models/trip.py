from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column, sessionmaker,relationship,selectinload
from decimal import Decimal
from app.database.base import Base
from app.models.driver import Driver
from sqlalchemy import ForeignKey

class Trip(Base):
    __tablename__="trips"
    id:Mapped[int]=mapped_column(primary_key=True)
    driver_id:Mapped[int]=mapped_column(ForeignKey("drivers.id"))
    driver:Mapped["Driver"]=relationship(back_populates="trips")
