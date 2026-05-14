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
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"


settings = Settings()
