"""Описание модели донатов."""
from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base, Charity


class Donation(Base, Charity):
    """
    Передадим родительский класс Charity.
    Пользователей вычислим по id.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
