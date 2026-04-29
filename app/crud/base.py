from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import QRKotBase

ModelType = TypeVar("ModelType", bound=QRKotBase)


class CRUDBase(Generic[ModelType]):
    """Базовый CRUD класс с общими операциями."""

    def __init__(self, model: type[ModelType]):
        """Инициализация CRUD."""
        self.model = model

    async def get_by_id(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """Получить проект по ID."""
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получить все проекты."""
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получить все незавершённые проекты."""
        result = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def create(
        self,
        obj_data: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Создать новый проект."""
        obj = self.model(
            **obj_data,
            invested_amount=0,
            fully_invested=False,
        )
        session.add(obj)
        if commit:
            await session.commit()
            await session.refresh(obj)
        return obj

    async def update(
        self,
        obj: ModelType,
        update_data: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> ModelType:
        """Обновить проект."""
        for key, value in update_data.items():
            setattr(obj, key, value)
        if commit:
            await session.commit()
            await session.refresh(obj)
        return obj

    async def delete(
        self,
        obj: ModelType,
        session: AsyncSession,
    ) -> None:
        """Удалить проект."""
        await session.delete(obj)
        await session.commit()
