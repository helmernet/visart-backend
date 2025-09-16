from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    fecha_creacion: datetime
    es_activo: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class PostBase(BaseModel):
    titulo: str
    contenido: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    fecha_creacion: datetime
    usuario_id: int
    
    class Config:
        from_attributes = True