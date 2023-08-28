"""Описание модели проектов."""
from sqlalchemy import Column, String, Text

from app.core.db import Base, Charity

from app.core.config import settings


class CharityProject(Base, Charity):
    """Передадим родительский класс Charity и опишем name и description."""
    name = Column(String(
        settings.max_string_length),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
