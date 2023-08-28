"""
Теперь все новые модели нужно будет импортировать в файл app/core/base.py.
Импорты класса Base и всех моделей для Alembic.
"""
from app.core.db import Base # noqa
from app.models import CharityProject, Donation, User# noqa
