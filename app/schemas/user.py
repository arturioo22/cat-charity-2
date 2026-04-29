from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, field_validator


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения данных пользователя."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя."""

    email: EmailStr


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных пользователя."""

    email: Optional[EmailStr] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: Optional[EmailStr]) -> Optional[EmailStr]:
        """Валидация email."""
        if value is not None and '@' not in str(value):
            raise ValueError('value is not a valid email address')
        return value
