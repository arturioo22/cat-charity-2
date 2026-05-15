from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
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
    try:
        spreadsheet_id, spreadsheet_url = await create_spreadsheets()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Файл с учётными данными Google API не найден: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Ошибка в настройках Google API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Не удалось создать Google таблицу: {str(e)}"
        )

    try:
        await update_spreadsheets_value(spreadsheet_id, session)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Не удалось заполнить Google таблицу данными: {str(e)}"
        )

    return {
        "status": "success",
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_url": spreadsheet_url,
        "message": "Отчёт успешно создан",
    }
