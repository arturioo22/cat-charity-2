from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import NAME_LENGTH
from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    """Модель благотворительного проекта."""

    __tablename__ = "charityproject"

    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
