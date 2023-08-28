"""
Процесс «инвестирования»
Сразу после создания нового проекта или пожертвования должен запускаться
процесс «инвестирования» (увеличение invested_amount как в пожертвованиях,
так и в проектах, установка значений fully_invested и close_date,
при необходимости).
Если создан новый проект, а в базе были «свободные»
(не распределённые по проектам) суммы пожертвований — они автоматически должны
инвестироваться в новый проект, и в ответе API эти суммы должны быть учтены.
То же касается и создания пожертвований: если в момент пожертвования есть
открытые проекты, эти пожертвования должны автоматически зачислиться
на их счета.
"""
from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.core.config import settings


async def get_not_full_invested_objects(
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    """
    Получаем список всех не закрытых объектов.
    """
    objects = await session.execute(
        select(obj_in).where(
            obj_in.fully_invested == settings.zero_count).order_by(
            obj_in.create_date
        )
    )
    return objects.scalars().all()


async def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    """
    Закрываем проект.
    Обновляем сумму в invested_amount
    Меняем значение в fully_invested
    Проставляем дату закрытия в close_date
    """
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def investing(
        obj_in: Union[CharityProject, Donation],
        obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    """
    Сохраняем для сравнения "свободные деньги" в переменные для:
    - объекта obj_in
    - объекта obj_model
    Далее начинаем сравнивать, от этого зависит куда пойдем и
    кому занесем деньги, в obj_in или obj_model.
    Затем для закрытия вызываем close_donation_for_obj.
    """
    free_money_in = obj_in.full_amount - obj_in.invested_amount
    free_money_in_model = obj_model.full_amount - obj_model.invested_amount

    if free_money_in > free_money_in_model:
        obj_in.invested_amount += free_money_in_model
        await close_donation_for_obj(obj_model)

    elif free_money_in == free_money_in_model:
        await close_donation_for_obj(obj_in)
        await close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += free_money_in
        await close_donation_for_obj(obj_in)
    return obj_in, obj_model


async def investing_process(
        obj_in: Union[CharityProject, Donation],
        obj_model_add: Union[CharityProject, Donation],
        session: AsyncSession,
) -> Union[CharityProject, Donation]:
    """
    Процесс инвестирования.

    Получаем на вход объект запроса и модель.
    Забираем из базы все не закрытые объекты.
    По одному передаем в инвест-функцию.
    Через session, находясь в цикле, добавляем в базу.
    Вышли, комитим и рефреш для обновления результата на выдачу.
    """
    objects_model = await get_not_full_invested_objects(obj_model_add, session)
    for obj_model in objects_model:
        obj_in, obj_model = await investing(obj_in, obj_model)
        session.add(obj_in)
        session.add(obj_model)

    await session.commit()
    await session.refresh(obj_in)
    return obj_in
