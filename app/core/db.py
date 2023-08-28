"""Здесь будет храниться код, ответственный за подключение к базе данных."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """
    Чтобы не повторяться в описании каждой модели — расширим базовый
    класс так, чтобы приватный атрибут __tablename__ и поле ID
    создавались автоматически.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class Charity:
    """Родительский класс для моделей."""
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=settings.zero_count)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Создадим функцию, которая будет использоваться как зависимость.

    Эта функция должна открывать сессии, а после выполнения всех операций,
    использующих эту сессию, или при ошибке — закрывать её.
    Чтобы зависимость выполнила какие-то действия после окончания обработки
    HTTP-запроса (в нашем случае — закрыла сессию), применяют ключевое
    слово yield.
    Асинхронная функция, в которой содержится ключевое слово yield,
    называется «асинхронным генератором».
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
