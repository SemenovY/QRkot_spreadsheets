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
from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.donation import donation_crud
from app.schemas.donation import DonationDbAdmin

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDbAdmin],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
# @router.get(
#     '/',
#     response_model=list[dict[str, int]],
#     dependencies=[Depends(current_superuser)],
# )
async def get_report(
        # create_date: datetime,
        # close_date: datetime,
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """
    Только для суперюзеров.
    """
    donations = await donation_crud.get_projects_by_completion_rate(session)

    return donations
