from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Visart Backend",
    description="API para la plataforma de generación de videos Visart",
    version="0.1.0"
)

app.include_router(api_router)