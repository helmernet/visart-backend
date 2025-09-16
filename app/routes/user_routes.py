from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_active_user
from app import security

# ✅ Importaciones corregidas
from app.models.user_models import User
from app.schemas.user_schemas import UserResponse, UserUpdate

# ✅ Router correctamente configurado
router = APIRouter(prefix="/users", tags=["users"])

# ✅ Endpoint para obtener usuario actual
@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtener información del usuario actualmente autenticado
    """
    return current_user

# ✅ Endpoint para actualizar usuario
@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar información del usuario actual
    """
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "username" in update_data and update_data["username"] != current_user.username:
        existing_user = db.query(User).filter(
            User.username == update_data["username"]
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )
    
    if "email" in update_data and update_data["email"] != current_user.email:
        existing_user = db.query(User).filter(
            User.email == update_data["email"]
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
    
    # Actualizar campos
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

# ✅ Endpoint para eliminar (desactivar) usuario
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar (desactivar) la cuenta del usuario actual
    """
    current_user.is_active = False
    db.commit()
    return None

# ✅ Endpoint para obtener usuario por ID (solo admin o propio usuario)
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información de un usuario específico
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Solo permitir ver el propio perfil o si es admin
    if user.id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    return user
