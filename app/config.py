import os
from dotenv import load_dotenv
from pydantic import AnyUrl, EmailStr, Field, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = Field(..., description="App environment (development/qa/production/staging)")
    DEBUG: bool = Field(..., description="Debug mode")
    DATABASE_URL: AnyUrl = Field(..., description="PostgreSQL connection string")
    SECRET_KEY: str = Field(..., min_length=32, description="Secret key for JWT")
    ADMIN_EMAIL: EmailStr = Field(..., description="Admin email")
    LOG_LEVEL: str = Field(..., description="Application log level")
    TOKEN_EXPIRE_MINUTES: int = Field(..., ge=1, le=1440, description="JWT token expiration time in minutes")
    SMTP_SERVER: str = Field(..., description="SMTP server address")
    SMTP_PORT: int = Field(..., ge=1, le=65535, description="SMTP port number")
    EMAIL_HOST: str = Field(..., description="Email host")
    EMAIL_PORT: int = Field(..., ge=1, le=65535, description="Email port")
    EMAIL_USER: str = Field(..., description="Email user")
    EMAIL_PASS: str = Field(..., description="Email password")
    ALLOWED_ORIGINS: str = Field(..., description="Allowed CORS origins")  # comma separated

    @field_validator("ENV")
    def validate_env(cls, v):
        assert v in ["development", "qa", "production", "staging"], "ENV must be development, qa, production or staging"
        return v

def load_settings(env_file: str = ".env") -> Settings:
    load_dotenv(env_file)
    return Settings()

# Ejemplo de uso:
# settings = load_settings(".env.dev")    # Desarrollo
# settings = load_settings(".env.qa")     # QA
# settings = load_settings(".env.prod")   # Production
# settings = load_settings(".env.staging") # Staging