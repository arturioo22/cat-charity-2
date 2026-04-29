from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    """Схема для создания нового пожертвования."""

    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None


class DonationDB(BaseModel):
    """Базовая схема пожертвования с данными из БД."""

    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True


class DonationFullInfoDB(DonationDB):
    """Расширенная схема пожертвования с информацией об инвестировании."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
