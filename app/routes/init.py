# app/routes/__init__.py
from .auth import router as auth_router
from .user_routes import router as users_router  # ✅ Cambiado de .users
from .posts import router as posts_router

__all__ = ["auth_router", "users_router", "posts_router"]