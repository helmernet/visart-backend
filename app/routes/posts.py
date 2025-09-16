from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.session import get_db
from app.models.user_models import User
from app.models.posts import Post  # ✅ Corregida la importación
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.dependencies import get_current_active_user

router = APIRouter(tags=["posts"])  # ✅ Eliminado el prefix para evitar duplicación

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear una nueva publicación"""
    try:
        new_post = Post(
            title=post.title,
            content=post.content,
            image_url=post.image_url,
            is_published=post.is_published,
            owner_id=current_user.id
        )
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la publicación: {str(e)}"
        )

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Obtener una publicación específica por ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    return post

@router.get("/", response_model=List[PostResponse])
def list_posts(
    skip: int = 0, 
    limit: int = 10, 
    is_published: bool = True,
    db: Session = Depends(get_db)
):
    """Listar publicaciones con paginación"""
    posts = db.query(Post).filter(Post.is_published == is_published).offset(skip).limit(limit).all()
    return posts

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, 
    post_update: PostUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar una publicación existente"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar que el usuario es el propietario
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta publicación"
        )
    
    # Actualizar solo los campos proporcionados
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db_post.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Eliminar una publicación"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publicación no encontrada"
        )
    
    # Verificar que el usuario es el propietario
    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta publicación"
        )
    
    db.delete(db_post)
    db.commit()
    return None