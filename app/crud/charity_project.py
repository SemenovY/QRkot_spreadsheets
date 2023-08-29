"""
Определим класс для CRUDCharityProject.
Использовать будем декоратор.
Через асинк и функцию проверка имени проекта.
Если в базе будет найден объект с таким же name — функция вернёт id
этого объекта; возвращать весь объект целиком нет смысла, ведь
цель — просто узнать, есть ли в базе такой объект.
Если в базе нет одноимённого проекта — функция вернёт None.
"""
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_project_id_by_name(
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Проверяем уникальность имени проекта."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, str]]:
        """
        Метод отсортирует список со всеми закрытыми проектами.
        """

        objects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested)
        )
        objects_list = []
        objects = objects.scalars().all()
        for object in objects:
            objects_list.append(
                {
                    'Название проекта': object.name,
                    'Время сбора': str(
                        object.close_date - object.create_date
                        ),
                    'Описание': object.description
                }
            )
            return objects_list


charity_project_crud = CRUDCharityProject(CharityProject)
