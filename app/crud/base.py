"""
Теперь мы для любой новой модели можем сразу подключить пять CRUD-методов,
создав объект класса CRUDBase и передав в него нужную модель.
Если для какой-то модели нужно реализовать уникальные методы, которые
неприменимы к другим моделям — создаём класс-наследник базового класса,
добавляем в него нужный метод — и создаём объект уже
на основе этого нового класса.
"""
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:
    """
    Базовый класс.
    """
    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession,):
        """Функция для получения объекта по его ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession,):
        """Функция будет считывать из базы все проекты."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        """
        Функция создания объекта.

        Сначала конвертируем в обычный словарь.
        Затем работа с базой данных.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession,):
        """
        Функция обновления объекта.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession,):
        """
        Функция удаления объекта.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: Union[str, bool],
        session: AsyncSession,
    ):
        """
        Получаем объект по заданному атрибуту.
        """
        attr = getattr(self.model, attr_name)
        order_attr = getattr(self.model, 'create_date')
        db_obj = await session.execute(
            select(self.model)
            .where(attr == attr_value)
            .with_for_update()
            .order_by(order_attr)
        )
        return db_obj.scalars().all()
