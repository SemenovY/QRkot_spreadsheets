"""
Определяем транспорт: передавать токен будем через заголовок HTTP-запроса
Authorization: Bearer.
Определяем стратегию: хранение токена в виде JWT.
Указываем URL эндпоинта для получения токена.
Создаём объект бэкенда аутентификации с выбранными параметрами.
"""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.loggers import logger
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Отдаем пользователя."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    В специальный класс из настроек приложения
    передаётся секретное слово, используемое для генерации токена.
    Вторым аргументом передаём срок действия токена в секундах.
    """

    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=settings.lifetime_seconds
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Здесь можно описать свои условия валидации пароля.
    При успешной валидации функция ничего не возвращает.
    При ошибке валидации будет вызван специальный класс ошибки
    InvalidPasswordException.
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < settings.min_password_length:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        logger.info(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Корутина, возвращающая объект класса UserManager.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend],)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
