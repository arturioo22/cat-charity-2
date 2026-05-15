import copy
from datetime import datetime
from typing import Any, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import (
    GOOGLE_SPREADSHEET_BODY_TEMPLATE,
    SECONDS_IN_HOUR,
    SECONDS_IN_MINUTE,
)
from app.core.google_client import get_service
from app.models.charity_project import CharityProject
from app.schemas.report import ProjectReportData


async def get_projects_by_completion_rate(
    session: AsyncSession
) -> List[ProjectReportData]:
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
        data = ProjectReportData(
            name=project.name,
            description=project.description,
            create_date=project.create_date,
            close_date=project.close_date,
        )
        projects_with_time.append((data, data.collection_time))

    projects_with_time.sort(key=lambda x: x[1])

    return [project for project, _ in projects_with_time]


async def create_spreadsheets() -> tuple[str, str]:
    """Создаёт Google таблицу с отчётом."""
    async for sheets_service, drive_service in get_service():
        spreadsheet_body = copy.deepcopy(GOOGLE_SPREADSHEET_BODY_TEMPLATE)
        spreadsheet_body["properties"]["title"] = (
            f"Отчёт фонда QRKot от "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        response = sheets_service.spreadsheets().create(
            body=spreadsheet_body,
            fields="spreadsheetId,spreadsheetUrl"
        ).execute()

        spreadsheet_id = response.get("spreadsheetId")
        spreadsheet_url = response.get("spreadsheetUrl")

        if not spreadsheet_id:
            raise ValueError("Не удалось получить ID созданной таблицы")

        if settings.email:
            await set_user_permissions(spreadsheet_id, drive_service)

        return spreadsheet_id, spreadsheet_url
    raise RuntimeError("Не удалось получить сервисы Google API")


async def set_user_permissions(
        spreadsheet_id: str, drive_service: Any
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
    async for sheets_service, _ in get_service():
        projects = await get_projects_by_completion_rate(session)

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values: List[List[str]] = [
            [f"Отчёт от {now_str}", "", ""],
            ["Топ проектов по скорости закрытия", "", ""],
            ["Название проекта", "Время сбора", "Описание"],
        ]

        for project in projects:
            days = project.collection_time.days
            seconds = project.collection_time.seconds
            hours = seconds // SECONDS_IN_HOUR
            minutes = (seconds % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
            secs = seconds % SECONDS_IN_MINUTE

            if days > 0:
                time_str = (
                    f"{days} day, {hours:02d}:{minutes:02d}:{secs:02d}."
                    f"{project.collection_time.microseconds:06d}"
                )
            else:
                time_str = (
                    f"{hours:02d}:{minutes:02d}:{secs:02d}."
                    f"{project.collection_time.microseconds:06d}"
                )

            values.append([project.name, time_str, project.description or ""])

        body: dict[str, Any] = {"values": values}
        sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="A1:C",
            valueInputOption="RAW",
            body=body,
        ).execute()
        break
