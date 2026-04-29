import asyncio

from app.core.auth import get_user_db, get_user_manager
from app.core.db import AsyncSessionLocal
from app.schemas.user import UserCreate


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
) -> None:
    """Создание пользователя."""
    async with AsyncSessionLocal() as session:
        user_db = await anext(get_user_db(session))
        user_manager = await anext(get_user_manager(user_db))

        user_create = UserCreate(
            email=email,
            password=password,
            is_superuser=is_superuser,
            is_active=True,
            is_verified=False,
        )
        await user_manager.create(user_create)


if __name__ == "__main__":
    asyncio.run(create_user("admin@example.com", "admin", is_superuser=True))
