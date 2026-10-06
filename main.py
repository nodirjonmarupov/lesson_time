from fastapi import FastAPI
from app.routers.drivers import router
from app.models.driver import Driver
from app.models.trip import Trip

app = FastAPI()

app.include_router(router, prefix="/drivers")