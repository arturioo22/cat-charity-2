import os
from typing import Any, AsyncGenerator, Dict, List, Tuple

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from app.core.config import settings


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


def get_credentials() -> Credentials:
    """Получение учётных данных для Google API."""
    creds_file = settings.google_credentials_file
    if creds_file is None:
        creds_file = "service_account.json"

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    creds_path = os.path.join(base_dir, creds_file)

    credentials = Credentials.from_service_account_file(
        creds_path,
        scopes=SCOPES,
    )

    return credentials


async def get_service() -> AsyncGenerator[Tuple[Any, Any], None]:
    """Возвращает сервисы Google Sheets и Google Drive."""
    credentials = get_credentials()

    sheets_service = build("sheets", "v4", credentials=credentials)
    drive_service = build("drive", "v3", credentials=credentials)

    yield sheets_service, drive_service
