from typing import Any, Dict, List, Tuple

from googleapiclient.discovery import Resource

from app.core.config import settings
from app.services.google_api import get_google_services

SCOPES: List[str] = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

INFO: Dict[str, Any] = {
    "type": settings.type or "service_account",
    "project_id": settings.project_id or "test",
    "private_key_id": settings.private_key_id or "test",
    "private_key": settings.private_key or "test",
    "client_email": settings.client_email or "test@test.com",
    "client_id": settings.client_id or "test",
    "auth_uri": settings.auth_uri or (
        "https://accounts.google.com/o/oauth2/auth"
    ),
    "token_uri": settings.token_uri or "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": settings.auth_provider_x509_cert_url or (
        "https://www.googleapis.com/oauth2/v1/certs"
    ),
    "client_x509_cert_url": settings.client_x509_cert_url or "",
}


def get_service() -> Tuple[Resource, Resource]:
    """Возвращает сервисы Google Sheets и Google Drive."""
    return get_google_services()