"""
Определим класс для CRUDCharityProject.
Использовать будем декоратор.
Через асинк и функцию проверка имени проекта.
Если в базе будет найден объект с таким же name — функция вернёт id
этого объекта; возвращать весь объект целиком нет смысла, ведь
цель — просто узнать, есть ли в базе такой объект.
Если в базе нет одноимённого проекта — функция вернёт None.
"""
from datetime import timedelta
from typing import Dict, List, Optional, Union

from sqlalchemy import func, select, true
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
    ) -> List[Dict[str, Union[str, timedelta]]]:
        """
        Метод отсортирует список со всеми закрытыми проектами.
        """

        projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested)
        )
        projects = projects.scalars().all()

        close_projects = []
        for project in projects:

            collection_time = (
                (func.julianday(CharityProject.close_date)
                 - func.julianday(CharityProject.create_date))
                .label('collection time')
            )

            close_projects.append(
                {'Название проекта': project.name,
                 'Время сбора': str(project.close_date - project.create_date),
                 'Описание': project.description}
            )
            close_projects = await session.execute(
                select(
                    CharityProject.name,
                    collection_time,
                    CharityProject.description
                ).where(
                    CharityProject.fully_invested == true()
                ).order_by('collection time')
            )
            close_projects = close_projects.all()

            return close_projects


charity_project_crud = CRUDCharityProject(CharityProject)
