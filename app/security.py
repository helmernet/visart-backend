"""
Utilidades de seguridad para Visart Backend
Manejo de contraseñas y tokens JWT
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-muy-segura-aqui-cambia-esto-en-produccion")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña en texto plano coincide con el hash almacenado
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para la contraseña
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crea un token JWT de acceso
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifica y decodifica un token JWT
    Retorna el payload si es válido, None si no lo es
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def create_refresh_token(data: dict) -> str:
    """
    Crea un token de refresh con mayor tiempo de expiración
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)  # 7 días de expiración
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_username_from_token(token: str) -> str:
    """
    Extrae el username del token JWT
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None

def validate_token(token: str) -> bool:
    """
    Valida si un token JWT es válido
    """
    payload = verify_token(token)
    return payload is not None

# Funciones para manejo de permisos (opcional)
def has_permission(token: str, required_permission: str) -> bool:
    """
    Verifica si el usuario tiene un permiso específico
    """
    payload = verify_token(token)
    if not payload:
        return False
    
    user_permissions = payload.get("permissions", [])
    return required_permission in user_permissions

def is_admin_user(token: str) -> bool:
    """
    Verifica si el usuario es administrador
    """
    payload = verify_token(token)
    if not payload:
        return False
    
    return payload.get("is_admin", False)