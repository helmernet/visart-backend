from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import load_settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visart-backend")

# Cargar configuración
settings = load_settings()

# Crear motor de base de datos
engine = create_engine(str(settings.DATABASE_URL), echo=settings.DEBUG)

# Crear session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importar routers disponibles
try:
    from app.routes.posts import router as posts_router
    from app.routes.user_routes import router as user_routes_router
    from app.routes.auth import router as auth_router
    from app.routes.health import router as health_router
    HAS_ROUTERS = True
except ImportError as e:
    logger.warning(f"Algunos routers no disponibles: {e}")
    HAS_ROUTERS = False

# Crear aplicación FastAPI
app = FastAPI(
    title="Visart Backend API",
    version="1.0.0",
    description="API para la generación de videos con IA"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "🎬 Visart Backend API", 
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "users": "/api/users",
            "auth": "/api/auth",
            "posts": "/api/posts"
        }
    }

# Health check endpoint
@app.get("/api/health")
async def health_check():
    try:
        return {
            "status": "healthy", 
            "service": "visart-backend",
            "environment": settings.ENV,
            "routers_loaded": HAS_ROUTERS
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Configuration error")

# Incluir routers si están disponibles
if HAS_ROUTERS:
    app.include_router(health_router, prefix="/api", tags=["health"])
    app.include_router(posts_router, prefix="/api/posts", tags=["posts"])
    app.include_router(user_routes_router, prefix="/api", tags=["users"])
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
else:
    logger.warning("Algunos routers no se cargaron")

# Middleware para logging
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Peticion: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Respuesta: {response.status_code} para {request.method} {request.url}")
    return response

# Si se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)