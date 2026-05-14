import os
from datetime import datetime
from typing import Any, List, Tuple

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.charity_project import CharityProject


async def get_projects_by_completion_rate(
    session: AsyncSession
) -> List[CharityProject]:
    """Возвращает список проектов, отсортированных от быстрых к медленным."""
    result = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(True),
            CharityProject.close_date.is_not(None),
        )
    )
    projects_list = list(result.scalars().all())

    projects_with_time = []
    for project in projects_list:
        collection_time = project.close_date - project.create_date
        projects_with_time.append((project, collection_time))

    projects_with_time.sort(key=lambda x: x[1])

    sorted_projects = [project for project, _ in projects_with_time]
    return sorted_projects


def get_google_credentials() -> Credentials:
    """Получение учётных данных для Google API."""
    assert settings.google_credentials_file is not None, (
        "GOOGLE_CREDENTIALS_FILE не указан"
    )

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    creds_path = os.path.join(base_dir, settings.google_credentials_file)

    credentials = Credentials.from_service_account_file(
        creds_path,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
        ],
    )

    return credentials


def get_google_services() -> Tuple[Resource, Resource]:
    """Возвращает сервисы Google Sheets и Google Drive."""
    credentials = get_google_credentials()

    sheets_service = build("sheets", "v4", credentials=credentials)
    drive_service = build("drive", "v3", credentials=credentials)

    return sheets_service, drive_service


async def create_spreadsheets() -> Tuple[str, str]:
    """Создаёт Google таблицу с отчётом."""
    sheets_service, drive_service = get_google_services()

    spreadsheet_body = {
        "properties": {
            "title": (
                f"Отчёт фонда QRKot от "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

        }
    }

    spreadsheet = sheets_service.spreadsheets().create(
        body=spreadsheet_body,
        fields="spreadsheetId"
    ).execute()

    spreadsheet_id = spreadsheet.get("spreadsheetId")
    if not spreadsheet_id:
        raise ValueError("Не удалось получить ID созданной таблицы")

    if settings.email:
        await set_user_permissions(spreadsheet_id, drive_service)

    spreadsheet_url = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
    )

    return spreadsheet_id, spreadsheet_url


async def set_user_permissions(
        spreadsheet_id: str, drive_service: Resource
) -> None:
    """Выдача прав личному аккаунту на доступ к таблице."""
    if settings.email and spreadsheet_id:
        permission = {
            "type": "user",
            "role": "writer",
            "emailAddress": settings.email,
        }
        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body=permission,
            fields="id",
            sendNotificationEmail=False,
        ).execute()


async def update_spreadsheets_value(
        spreadsheet_id: str, session: AsyncSession
) -> None:
    """Обновляет данные в Google таблице."""
    sheets_service, _ = get_google_services()

    projects = await get_projects_by_completion_rate(session)

    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    values: List[List[str]] = [
        [f"Отчёт от {now_str}", "", ""],
        ["Топ проектов по скорости закрытия", "", ""],
        ["Название проекта", "Время сбора", "Описание"],
    ]

    for project in projects:
        collection_time = project.close_date - project.create_date
        days = collection_time.days
        seconds = collection_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if days > 0:
            time_str = (
                f"{days} day, {hours:02d}:{minutes:02d}:{secs:02d}."
                f"{collection_time.microseconds:06d}"
            )
        else:
            time_str = (
                f"{hours:02d}:{minutes:02d}:{secs:02d}."
                f"{collection_time.microseconds:06d}"
            )

        values.append([project.name, time_str, project.description or ""])

    body: dict[str, Any] = {"values": values}
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="A1:C",
        valueInputOption="RAW",
        body=body,
    ).execute()
