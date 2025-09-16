import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("visart-backend")
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Petición: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Respuesta: {response.status_code} para {request.method} {request.url}")
        return response