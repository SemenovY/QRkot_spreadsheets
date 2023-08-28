"""
Эндпоинты для донатов.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import CharityProject, User
from app.schemas.donation import DonationDB, DonationDbAdmin, DonationCreate
from app.crud.donation import donation_crud
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDbAdmin],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)

    return all_donations


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список моих пожертвований.
    """
    my_donations = await donation_crud.get_by_user(user, session)

    return my_donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Сделать пожертвование.
    """
    new_donation = await donation_crud.create(donation, session, user)
    await investing_process(new_donation, CharityProject, session)

    return new_donation
