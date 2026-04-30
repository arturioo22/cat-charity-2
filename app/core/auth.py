from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.constants import MIN_PASSWORD_LENGTH
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей."""

    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User | None = None,
    ) -> None:
        """Валидация пароля."""
        if not password:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "code": "REGISTER_INVALID_PASSWORD",
                    "reason": "Пароль не может быть пустым",
                },
            )
        if len(password) < MIN_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "code": "REGISTER_INVALID_PASSWORD",
                    "reason": (
                        f"Пароль должен содержать не менее "
                        f"{MIN_PASSWORD_LENGTH} символов"
                    ),
                },
            )
        await super().validate_password(password, user)

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Действия после регистрации пользователя."""

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Действия после запроса сброса пароля."""

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Действия после запроса верификации."""


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Получение базы данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    """Получение менеджера пользователей."""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Получение JWT стратегии."""
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.jwt_lifetime_seconds,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
