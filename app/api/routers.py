"""
Создаем «объединяющей» роутер,
к которому будут подключены все нужные роутеры. И тогда в файле app/main.py
можно будет одной строкой подключить этот главный роутер.
В файле app/api/routers.py создайте главный роутер с именем main_router
и подключите к нему существующие роутеры из app/api/endpoints.
Объекты роутеров называются одинаково, router, так что при помощи
конструкции from ... import ... as ... присвоим им псевдонимы (alias).
"""
from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router, donation_router, google_api_router, user_router
)

main_router = APIRouter()

main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Charity Projects'],
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donations'],
)
main_router.include_router(
    google_api_router, prefix='/google', tags=['Google']
)

main_router.include_router(user_router)
