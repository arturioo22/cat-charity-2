import secrets

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = "Благотворительный фонд поддержки котиков QRKot"
    app_description: str = "Сервис для поддержки котиков"
    database_url: str = "sqlite+aiosqlite:///./qrkot.db"
    secret_key: str = secrets.token_urlsafe(32)

    class Config:
        """Конфигурация Pydantic."""

        env_file = ".env"


settings = Settings()
