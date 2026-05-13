from app.core.auth import auth_backend, get_user_db, get_user_manager
from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user, fastapi_users


def __getattr__(name):
    """Загрузка модулей для избежания циклических импортов."""
    if name == "google_client":
        from app.services.google_api import get_google_services
        return get_google_services()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "settings",
    "get_async_session",
    "get_user_db",
    "get_user_manager",
    "auth_backend",
    "fastapi_users",
    "current_user",
    "current_superuser",
    "google_client",
]
