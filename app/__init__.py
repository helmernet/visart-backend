"""
Paquete principal de la aplicación Visart Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visart-backend")

# Crear aplicación FastAPI
app = FastAPI(
    title="Visart Backend API",
    description="API para la generación de videos con IA",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Evento de startup
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    logger.info("Aplicación Visart Backend iniciada correctamente")

# Evento de shutdown  
@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al detener la aplicación"""
    logger.info("Aplicación Visart Backend detenida")