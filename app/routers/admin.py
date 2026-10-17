from fastapi import Depends,APIRouter
from app.dependencies import RoleChecker
from app.models.user import User


router=APIRouter(
    
    tags=["Admin Paneli"]

)

@router.get("/dashboard")
def get_admin_dashboard(current_user: User=Depends(RoleChecker(["admin"]))):
    return {
        "status": "success",
        "message": "Xush kelibsiz, Admin!",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role
        }
    }

@router.get("/driver-list")
def get_driver_list(current_user: User = Depends(RoleChecker(["admin", "driver"]))):
    return {
        "status": "success",
        "message": f"Salom {current_user.email}, sizga ruxsat berildi!",
        "your_role": current_user.role
    }