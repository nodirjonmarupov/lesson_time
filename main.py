from fastapi import FastAPI
from app.routers import auth, admin, drivers  # drivers ham o'z joyida tursin
from app.models.driver import Driver
from app.models.trip import Trip


app = FastAPI()

# Auth router
app.include_router(auth.router, prefix="/auth")

# Admin router (agar ichida /dashboard bo'lsa, /admin/dashboard bo'lib ochiladi)
app.include_router(admin.router, prefix="/admin")

# Drivers router (agar kerak bo'lsa)
app.include_router(drivers.router, prefix="/drivers")