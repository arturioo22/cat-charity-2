from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import (USER_EMAIL_MAX_LENGTH,
                                USER_PASSWORD_HASH_MAX_LENGTH)
from app.models.base import QRKotBase


class User(SQLAlchemyBaseUserTable[int], QRKotBase):
    """Модель пользователя."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=USER_EMAIL_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=USER_PASSWORD_HASH_MAX_LENGTH),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )