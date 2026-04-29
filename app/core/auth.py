from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
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
                status_code=400,
                detail={
                    "code": "REGISTER_INVALID_PASSWORD",
                    "reason": "Пароль не может быть пустым",
                }
            )
        if len(password) < 3:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "REGISTER_INVALID_PASSWORD",
                    "reason": "Пароль должен содержать не менее 3 символов",
                }
            )
        await super().validate_password(password, user)

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        """Действия после регистрации пользователя."""
        print(f"Пользователь {user.id} зарегистрирован.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Действия после запроса сброса пароля."""
        print(f"Пользователь {user.id} запросил сброс пароля. Токен: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Действия после запроса верификации."""
        print(
            f"Запрошена верификация для пользователя {user.id}. Токен: {token}"
        )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Получение базы данных пользователей."""
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    """Получение менеджера пользователей."""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Получение JWT стратегии."""
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
