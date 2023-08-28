"""
Основные проверки проекта.
 на совпадение имен
 для проверки повторяющегося id
 на возможность устанавливать для проекта новую требуемую сумму
 на удаление и редактирование проекта
"""
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(name: str, session: AsyncSession,) -> None:
    """Проверка в базе на совпадение имен."""
    project = await charity_project_crud.get_project_id_by_name(name, session)
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Отдельная функция для проверки повторяющегося id."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


def check_charity_project_invested_amount(
        project: CharityProject,
        obj_in: CharityProjectUpdate
) -> None:
    """
    Проверка возможности устанавливать для проекта новую требуемую
    сумму, но не меньше уже внесённой.
    """
    if obj_in.full_amount:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Нельзя Установить Общую сумму ниже накопленной!'
            )


def check_charity_project_before_delete(
        project: CharityProject, delete=False
) -> None:
    """Проверка перед удалением проекта, в который внесены средства."""
    if delete and project.invested_amount > settings.zero_count:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_closed(
        project: CharityProject,
) -> None:
    """
    Проверка проекта на закрытие, перед редактированием.
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
