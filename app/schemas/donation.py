"""Pydantic схемы для донатов, для Post and Get запросов."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Extra


class DonationCreate(BaseModel):
    """Схема DonationCreate, для Post запроса."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        """
        Чтобы запретить пользователю передавать параметры,
        не описанные в схеме, в подклассе Config устанавливается
        значение extra = Extra.forbid
        """
        extra = Extra.forbid


class DonationDB(DonationCreate):
    """Для гет и для пост."""
    id: int
    create_date: datetime

    class Config:
        """
        Чтобы запретить пользователю передавать параметры,
        не описанные в схеме, в подклассе Config устанавливается
        значение extra = Extra.forbid
        """
        orm_mode = True


class DonationDbAdmin(DonationDB):
    """Для пользователей с правами администратора."""
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
