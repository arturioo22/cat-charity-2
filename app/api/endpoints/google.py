from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models.user import User
from app.services.google_api import (create_spreadsheets,
                                     update_spreadsheets_value)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    "/google/",
    status_code=HTTPStatus.OK,
)
async def create_report(
    session: SessionDep,
    user: User = Depends(current_superuser),
) -> dict:
    """
    Создаёт Google таблицу с отчётом о закрытых проектах.
    Только для суперпользователей.
    """
    spreadsheet_id, spreadsheet_url = await create_spreadsheets()
    await update_spreadsheets_value(spreadsheet_id, session)

    return {
        "status": "success",
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_url": spreadsheet_url,
        "message": "Отчёт успешно создан",
    }
