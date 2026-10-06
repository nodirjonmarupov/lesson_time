from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column, sessionmaker,relationship,selectinload
from decimal import Decimal
from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.trip import Trip

class Driver(Base):
    __tablename__="drivers"
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(nullable=False)
    is_online:Mapped[bool]=mapped_column(default=False)
    rating:Mapped[Decimal]=mapped_column(default=4.5)
    phone: Mapped[str] = mapped_column(nullable=True,index=True)
    trips:Mapped[list["Trip"]]=relationship(back_populates="driver")