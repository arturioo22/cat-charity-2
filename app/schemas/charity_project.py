from datetime import datetime
from typing import Optional

from pydantic import QRKotBase, ConfigDict, Field, field_validator

from app.core.constants import (DESCRIPTION_MIN_LENGTH, FULL_AMOUNT_MIN_VALUE,
                                NAME_LENGTH, NAME_MIN_LENGTH)


class CharityProjectCreate(QRKotBase):
    """Схема для создания нового благотворительного проекта."""

    model_config = ConfigDict(extra='forbid')

    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_LENGTH,
    )
    description: str = Field(
        ...,
        min_length=DESCRIPTION_MIN_LENGTH,
    )
    full_amount: int = Field(
        ...,
        gt=FULL_AMOUNT_MIN_VALUE,
    )

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        """Проверяет, что название не состоит из одних пробелов."""
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        return value.strip()


class CharityProjectUpdate(QRKotBase):
    """Схема для обновления существующего благотворительного проекта."""

    model_config = ConfigDict(extra='forbid')

    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_LENGTH,
    )
    description: Optional[str] = Field(
        None,
        min_length=DESCRIPTION_MIN_LENGTH,
    )
    full_amount: Optional[int] = Field(
        None,
        gt=FULL_AMOUNT_MIN_VALUE,
    )


class CharityProjectDB(QRKotBase):
    """Схема для представления благотворительного проекта в базе данных."""

    id: int
    name: str
    description: str
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        """Конфигурация Pydantic."""

        from_attributes = True
