from typing import Optional

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    """Модель пожертвования с необязательным комментарием."""

    __tablename__ = "donation"

    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
