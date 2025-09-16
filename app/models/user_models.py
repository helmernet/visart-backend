"""
Modelos de usuario para la aplicación Visart
Este módulo define las estructuras de datos relacionadas con usuarios
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base  # ✅ Cambiado de app.database a app.db.base


class User(Base):
    """
    Modelo de usuario para el sistema Visart
    Representa a los usuarios registrados en la plataforma
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    
    # Relación con posts
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    
    # Relación con perfiles (uno a uno)
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Relación de seguidores (muchos a muchos)
    followers = relationship(
        "User", 
        secondary="user_follows",
        primaryjoin="User.id==UserFollows.followed_id",
        secondaryjoin="User.id==UserFollows.follower_id",
        backref="following"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserProfile(Base):
    """
    Modelo de perfil de usuario para información adicional
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    location = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Preferencias del usuario
    email_notifications = Column(Boolean, default=True)
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, full_name='{self.full_name}')>"


class UserFollows(Base):
    """
    Modelo para relaciones de seguimiento entre usuarios
    """
    __tablename__ = "user_follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Restricción única para evitar duplicados
    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
    )

    def __repr__(self):
        return f"<UserFollows(follower_id={self.follower_id}, followed_id={self.followed_id})>"


# Funciones de utilidad para operaciones con usuarios
def create_user(db, username: str, email: str, password: str, **kwargs):
    """
    Crea un nuevo usuario en la base de datos
    """
    from app.security import get_password_hash
    
    # Verificar si el usuario ya existe
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        return None
    
    hashed_password = get_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        **kwargs
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear perfil vacío para el usuario
    new_profile = UserProfile(user_id=new_user.id)
    db.add(new_profile)
    db.commit()
    
    return new_user


def get_user_by_username(db, username: str):
    """
    Obtiene un usuario por su nombre de usuario
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db, email: str):
    """
    Obtiene un usuario por su correo electrónico
    """
    return db.query(User).filter(User.email == email).first()


def verify_user_password(plain_password: str, hashed_password: str):
    """
    Verifica si la contraseña proporcionada coincide con el hash almacenado
    """
    from app.security import verify_password
    return verify_password(plain_password, hashed_password)


def update_user_last_login(db, user_id: int):
    """
    Actualiza la fecha del último inicio de sesión del usuario
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    return None