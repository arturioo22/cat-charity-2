from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class QRKotBase(DeclarativeBase):
    """Базовый абстрактный класс для всех моделей с общими полями."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return f"<{self.__class__.__name__}(id={self.id})>"


class InvestmentBase(QRKotBase):
    """Абстрактная модель для инвестиционных объектов."""

    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    close_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "full_amount > 0",
            name="check_full_amount_positive"
        ),
        CheckConstraint(
            "invested_amount >= 0",
            name="check_invested_amount_non_negative"
        ),
        CheckConstraint(
            "invested_amount <= full_amount",
            name="check_invested_amount_not_exceed_full_amount"
        ),
    )

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount}, "
            f"fully_invested={self.fully_invested})>"
        )
