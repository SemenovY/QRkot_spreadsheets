"""
Для донатов CRUD наследуем базовый, добавив метод получения юзера.
"""
from typing import List

from sqlalchemy import select
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

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        """
        Метод отсортирует список со всеми закрытыми проектами.
        """
        objects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested != settings.zero_count)
            .order_by(CharityProject.create_date))

        return objects.scalars().all()


donation_crud = CRUDdonation(Donation)
