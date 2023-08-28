"""Pydantic схемы для проектов, для Post and Get запросов."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import settings


class CharityProjectBase(BaseModel):
    """Создадим базовый класс схемы Charity."""

    class Config:
        """
        Чтобы запретить пользователю передавать параметры,
        не описанные в схеме, в подклассе Config устанавливается
        значение extra = Extra.forbid
        """
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """Схема CharityProject, для Post запроса."""

    name: str = Field(
        ...,
        min_length=settings.min_string_length,
        max_length=settings.max_string_length,
    )
    description: str = Field(..., min_length=settings.min_string_length)
    full_amount: PositiveInt = Field(..., title='Требуемая сумма')


class CharityProjectUpdate(CharityProjectBase):
    """
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """

    name: Optional[str] = Field(
        None,
        min_length=settings.min_string_length,
        max_length=settings.max_string_length,
    )
    description: Optional[str] = Field(
        None,
        min_length=settings.min_string_length,
    )
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectCreate):
    """Возвращаем ответ."""

    id: int
    invested_amount: int = Field(..., ge=settings.zero_count)
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        """
        Чтобы FastAPI мог сериализовать объект ORM-модели,
        в схеме CharityProjectDB, нужно указать, что схема может принимать
        на вход объект базы данных, а не только Python-словарь или JSON-объект.
        """

        orm_mode = True
