"""
Напишем «ручку», которая будет запускать процесс сбора информации из
базы данных и формирования отчёта в гугл-таблице.
Функция будет обрабатывать запрос, отправленный методом POST.
Эта функция будет принимать:
две даты — начало и конец временного интервала,
для которого будет подсчитываться количество бронирований;
объект AsyncSession для работы с асинхронными сессиями;
объект Aiogoogle — объект «обёртки», передаётся из настроек.
"""
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectDB
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    # response_model=list[dict[str, int]],
    response_model=List[CharityProjectDB],

    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Только для суперюзеров.
    """
    donations = await donation_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid,
        donations,
        wrapper_services
        )
    return donations
