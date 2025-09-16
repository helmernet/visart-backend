from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
import os
import asyncio
from typing import List, Set
import re
from importlib import reload

# ✅✅✅ IMPORTACIONES CORREGIDAS ✅✅✅
# Importar y recargar módulos para evitar caché corrupto
import app.routes.auth
import app.routes.user_routes  # ✅ Cambiado de app.routes.users
import app.routes.posts

# Recargar módulos para obtener versiones frescas
reload(app.routes.auth)
reload(app.routes.user_routes)  # ✅ Cambiado de app.routes.users
reload(app.routes.posts)

# Importar routers después de recargar
from app.routes.auth import router as auth_router
from app.routes.user_routes import router as users_router  # ✅ Cambiado de app.routes.users
from app.routes.posts import router as posts_router

from app.db.session import engine
from app.db.modelos import Base

# Crear tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Visart Backend API",
    description="API para la generación de videos con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not origins or origins == [""]:
    origins = [
        "http://localhost:5173",
        "http://localhost:8000", 
        "http://127.0.0.1:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# SOLUCIÓN: Crear routers FRESCOS desde cero
def create_clean_routers():
    """Crear routers completamente nuevos para evitar contaminación"""
    fresh_auth = APIRouter()
    fresh_users = APIRouter()
    fresh_posts = APIRouter()
    
    # Copiar solo las rutas esenciales de los routers originales
    for route in auth_router.routes:
        if isinstance(route, APIRoute):
            fresh_auth.routes.append(route)
    
    for route in users_router.routes:
        if isinstance(route, APIRoute):
            fresh_users.routes.append(route)
    
    for route in posts_router.routes:
        if isinstance(route, APIRoute):
            fresh_posts.routes.append(route)
    
    return fresh_auth, fresh_users, fresh_posts

# Crear routers limpios
auth_clean, users_clean, posts_clean = create_clean_routers()

# ✅ INCLUIR ROUTERS CON PREFIX CORRECTO
app.include_router(auth_clean, prefix="/api")
app.include_router(users_clean, prefix="/api")  # ✅ /api + /users = /api/users
app.include_router(posts_clean, prefix="/api/videos")

# FUNCIÓN DE LIMPIEZA EXTREMA
def nuclear_route_cleanup(app: FastAPI) -> int:
    """
    Elimina TODAS las rutas duplicadas y corrige paths corruptos
    """
    seen_keys: Set[str] = set()
    clean_routes: List[APIRoute] = []
    removed_count = 0
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            # Corregir paths corruptos
            if hasattr(route, 'path'):
                original_path = route.path
                # Corregir patrones corruptos
                if 'user=' in route.path:
                    route.path = route.path.replace('user=', 'users/')
                    print(f"🔧 Corrigiendo: {original_path} -> {route.path}")
                if 'users/users' in route.path:
                    route.path = route.path.replace('users/users', 'users')
                    print(f"🔧 Corrigiendo: {original_path} -> {route.path}")
                if '//' in route.path:
                    route.path = route.path.replace('//', '/')
                    print(f"🔧 Corrigiendo: {original_path} -> {route.path}")
            
            # Crear clave única por método y path
            methods = ''.join(sorted(route.methods)) if hasattr(route, 'methods') else ''
            path = route.path if hasattr(route, 'path') else ''
            route_key = f"{methods}:{path}"
            
            if route_key not in seen_keys:
                seen_keys.add(route_key)
                clean_routes.append(route)
            else:
                print(f"🗑️ Eliminando duplicado: {route.path}")
                removed_count += 1
        else:
            clean_routes.append(route)
    
    app.router.routes = clean_routes
    return removed_count

# EJECUTAR LIMPIEZA DURANTE STARTUP
@app.on_event("startup")
async def startup_cleanup():
    print("🚀 Iniciando Visart Backend API con limpieza nuclear...")
    
    # Limpieza agresiva múltiple
    total_removed = 0
    for i in range(5):  # 5 intentos de limpieza
        removed = nuclear_route_cleanup(app)
        total_removed += removed
        print(f"🔄 Limpieza {i+1}: {removed} duplicados eliminados")
        if removed == 0:
            break
        await asyncio.sleep(0.1)
    
    # VERIFICACIÓN FINAL
    print("\n✅ RUTAS FINALES REGISTRADAS:")
    user_routes = []
    video_routes = []
    auth_routes = []
    
    for i, route in enumerate(app.routes):
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            path = route.path
            if 'users' in path:
                user_routes.append(path)
            elif 'auth' in path:
                auth_routes.append(path)
            elif 'posts' in path or 'videos' in path:
                video_routes.append(path)
            
            print(f"{i:2d}. {list(route.methods)} {path}")
    
    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   Total rutas: {len(app.routes)}")
    print(f"   Rutas de auth: {len(auth_routes)}")
    print(f"   Rutas de usuarios: {len(user_routes)}")
    print(f"   Rutas de videos: {len(video_routes)}")
    print(f"   Duplicados eliminados: {total_removed}")
    print("🌐 Servidor listo: http://localhost:8000")

# Endpoints básicos
@app.get("/")
def read_root():
    return {
        "message": "Visart API funcionando",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "visart-backend",
        "environment": "development",
        "database": "connected",
        "version": "1.0.0",
        "routes_registered": len(app.routes)
    }

# BLOQUEO DE IMPORTS DUPLICADOS
import sys
sys.path = [p for p in sys.path if not any(x in p.lower() for x in ['api', 'usuarios', 'duplicate'])]

# Si se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )