import secrets
from typing import Optional

from pydantic_settings import BaseSettings

from app.core.constants import JWT_LIFETIME_SECONDS


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    app_description: str = "Сервис для поддержки котиков"
    database_url: str = "sqlite+aiosqlite:///./qrkot.db"
    secret_key: str = secrets.token_urlsafe(32)
    jwt_lifetime_seconds: int = JWT_LIFETIME_SECONDS
    google_credentials_file: Optional[str] = None
    email: Optional[str] = None

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"


settings = Settings()
