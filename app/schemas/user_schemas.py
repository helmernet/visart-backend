"""
Esquemas Pydantic para usuarios y perfiles
Define las estructuras de datos para validación y serialización de usuarios
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# Esquemas base
class UserBase(BaseModel):
    """Esquema base para usuario"""
    username: str
    email: EmailStr


# Esquemas para creación
class UserCreate(UserBase):
    """Esquema para creación de usuario"""
    password: str


class UserProfileCreate(BaseModel):
    """Esquema para creación de perfil de usuario"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    email_notifications: Optional[bool] = True


# Esquemas para actualización
class UserUpdate(BaseModel):
    """Esquema para actualización de usuario"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserProfileUpdate(BaseModel):
    """Esquema para actualización de perfil de usuario"""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    email_notifications: Optional[bool] = None


class UserPasswordUpdate(BaseModel):
    """Esquema para actualización de contraseña"""
    current_password: str
    new_password: str


# Esquemas para respuesta
class UserProfileResponse(BaseModel):
    """Esquema de respuesta para perfil de usuario"""
    id: int
    user_id: int
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    email_notifications: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    """Esquema de respuesta para usuario"""
    id: int
    is_active: bool
    fecha_creacion: datetime
    last_login: Optional[datetime] = None
    profile: Optional[UserProfileResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserPublicResponse(BaseModel):
    """Esquema de respuesta pública para usuario (sin información sensible)"""
    id: int
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Esquemas para autenticación
class UserLogin(BaseModel):
    """Esquema para inicio de sesión"""
    username: str
    password: str


class Token(BaseModel):
    """Esquema para token de acceso"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Esquema para datos del token"""
    username: Optional[str] = None


# Esquemas para relaciones de seguimiento
class FollowCreate(BaseModel):
    """Esquema para crear relación de seguimiento"""
    followed_id: int


class FollowResponse(BaseModel):
    """Esquema de respuesta para relación de seguimiento"""
    id: int
    follower_id: int
    followed_id: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Esquemas para estadísticas de usuario
class UserStatsResponse(BaseModel):
    """Esquema de respuesta para estadísticas de usuario"""
    user_id: int
    post_count: int
    follower_count: int
    following_count: int


# Esquemas para listas
class UserListResponse(BaseModel):
    """Esquema de respuesta para lista de usuarios"""
    users: List[UserPublicResponse]
    total_count: int
    page: int
    page_size: int


class FollowListResponse(BaseModel):
    """Esquema de respuesta para lista de seguidores/seguidos"""
    users: List[UserPublicResponse]
    total_count: int
    page: int
    page_size: int
    relationship_type: str  # 'followers' o 'following'


# Esquemas para búsqueda
class UserSearchFilters(BaseModel):
    """Esquema para filtros de búsqueda de usuarios"""
    username: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


# Esquemas para administración
class UserAdminResponse(UserResponse):
    """Esquema de respuesta para administradores (incluye información sensible)"""
    email: EmailStr
    is_admin: bool
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserAdminUpdate(BaseModel):
    """Esquema para actualización administrativa de usuario"""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    username: Optional[str] = None


# Esquemas para notificaciones
class UserNotificationSettings(BaseModel):
    """Esquema para configuraciones de notificaciones"""
    email_notifications: bool
    push_notifications: Optional[bool] = False
    newsletter_subscription: Optional[bool] = False