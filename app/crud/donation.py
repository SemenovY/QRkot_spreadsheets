"""
Для донатов CRUD наследуем базовый, добавив метод получения юзера.
"""
from datetime import datetime
from typing import List, Union

from sqlalchemy import and_, between, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.base import CRUDBase

from app.models import CharityProject, Donation
from app.models.user import User


class CRUDdonation(CRUDBase):
    """
    Создаём класс CRUDdonation (наследник CRUDBase).
    Расширяем этот класс методом get_by_user();
    """

    @staticmethod
    async def get_by_user(user: User, session: AsyncSession,):
        """Получаем из базы юзера по id."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        donations = donations.scalars().all()
        return donations

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        """
        Метод отсортирует список со всеми закрытыми проектами.
        """
        donations = await donation_crud.get_multi(session)
        return donations


donation_crud = CRUDdonation(Donation)
