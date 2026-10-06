from fastapi import APIRouter,Depends
from app.schemas.driver import CreateDriver
from app.database.connectoin import get_db
from sqlalchemy import select
from app.models.driver import Driver
from app.services.driver_service import get_drivers


router=APIRouter(tags=["Drivers"])


@router.get("/")
def get_drivers_endpoint(db=Depends(get_db)):
    return get_drivers(db)

@router.post("/")
async def create_driver(driver: CreateDriver):
    return driver