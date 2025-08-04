from fastapi import APIRouter
from app.api import user

router = APIRouter()
router.include_router(user.router)

@router.get("/")
def read_root():
    return {"message": "¡Visart Backend está funcionando correctamente!"}