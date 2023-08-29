"""
Для донатов CRUD наследуем базовый, добавив метод получения юзера.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase

from app.models import Donation
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


donation_crud = CRUDdonation(Donation)
