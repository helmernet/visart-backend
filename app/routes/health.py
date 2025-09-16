"""
Router para health checks
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("")
async def health_check(db: Session = Depends(get_db)):
    # Verificar conexión a la base de datos
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "service": "visart-backend"
    }

@router.get("/db")
async def health_check_db(db: Session = Depends(get_db)):
    """Health check específico para la base de datos"""
    try:
        result = db.execute("SELECT 1").scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Conexión a la base de datos exitosa"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }