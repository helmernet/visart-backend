from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError


async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Ha ocurrido un error interno. Por favor, intenta más tarde."}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    mensajes = []
    for err in errors:
        loc = " -> ".join([str(e) for e in err["loc"]])
        mensajes.append(f"{loc}: {err['msg']}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Error de validación de datos.",
            "detalles": mensajes
        }
    )

async def jwt_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=401,
        content={"error": "Token de autenticación inválido o expirado."}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, internal_server_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(JWTError, jwt_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)