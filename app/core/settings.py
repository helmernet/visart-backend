from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    secret_key: str = Field(..., env="SECRET_KEY")
    debug: bool = Field(False, env="DEBUG")
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"], env="ALLOWED_ORIGINS")

    email_host: str = Field(..., env="EMAIL_HOST")
    email_port: int = Field(..., env="EMAIL_PORT")
    email_user: str = Field(..., env="EMAIL_USER")
    email_pass: str = Field(..., env="EMAIL_PASS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Procesa allowed_origins como lista desde string
    @classmethod
    def parse_allowed_origins(cls, origins: str) -> List[str]:
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

    def __init__(self, **values):
        super().__init__(**values)
        # Si allowed_origins es un string, lo convierte a lista
        if isinstance(self.allowed_origins, str):
            self.allowed_origins = self.parse_allowed_origins(self.allowed_origins)

settings = Settings()