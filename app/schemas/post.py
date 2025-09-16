"""
Esquemas Pydantic para publicaciones (posts)
Define las estructuras de datos para validación y serialización de publicaciones
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# Esquemas base
class PostBase(BaseModel):
    """Esquema base para publicación"""
    title: str
    content: str
    image_url: Optional[str] = None
    is_published: Optional[bool] = True


# Esquemas para creación
class PostCreate(PostBase):
    """Esquema para creación de publicación"""
    pass


# Esquemas para actualización
class PostUpdate(BaseModel):
    """Esquema para actualización de publicación"""
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None


# Esquemas para respuesta - Propietario
class PostOwnerResponse(BaseModel):
    """Esquema simplificado del propietario para respuesta de publicación"""
    id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Esquemas para respuesta - Publicación
class PostResponse(PostBase):
    """Esquema de respuesta para publicación"""
    id: int
    owner_id: int
    owner: PostOwnerResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PostDetailResponse(PostResponse):
    """Esquema de respuesta detallada para publicación"""
    likes_count: Optional[int] = 0
    comments_count: Optional[int] = 0
    is_liked: Optional[bool] = False
    is_owner: Optional[bool] = False


# Esquemas para listas
class PostListResponse(BaseModel):
    """Esquema de respuesta para lista de publicaciones"""
    posts: List[PostResponse]
    total_count: int
    page: int
    page_size: int


# Esquemas para interacciones (likes)
class LikeCreate(BaseModel):
    """Esquema para crear like"""
    post_id: int


class LikeResponse(BaseModel):
    """Esquema de respuesta para like"""
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Esquemas para comentarios
class CommentBase(BaseModel):
    """Esquema base para comentario"""
    content: str


class CommentCreate(CommentBase):
    """Esquema para creación de comentario"""
    post_id: int


class CommentOwnerResponse(BaseModel):
    """Esquema simplificado del propietario para respuesta de comentario"""
    id: int
    username: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class CommentResponse(CommentBase):
    """Esquema de respuesta para comentario"""
    id: int
    post_id: int
    user_id: int
    user: CommentOwnerResponse
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    """Esquema para actualización de comentario"""
    content: str


# Esquemas para búsqueda y filtros
class PostSearchFilters(BaseModel):
    """Esquema para filtros de búsqueda de publicaciones"""
    title: Optional[str] = None
    content: Optional[str] = None
    username: Optional[str] = None
    is_published: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# Esquemas para estadísticas
class PostStatsResponse(BaseModel):
    """Esquema de respuesta para estadísticas de publicación"""
    post_id: int
    likes_count: int
    comments_count: int
    views_count: Optional[int] = 0


# Esquemas para feeds y timelines
class FeedFilters(BaseModel):
    """Esquema para filtros de feed"""
    followed_only: Optional[bool] = True
    page: Optional[int] = 1
    page_size: Optional[int] = 20