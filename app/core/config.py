"""
В директории проекта /app каталог /core (в переводе с английского — «ядро»).

Будет хранить файлы, отвечающие за «ядро» проекта — общие настройки приложения,
файлы для работы с БД и другие файлы, отвечающие за конфигурацию проекта.
"""
from typing import Optional

from pydantic import BaseSettings, EmailStr

DEFAULT_MIN_PASSWORD_LENGTH = 3
DEFAULT_MIN_STRING_LENGTH = 1
DEFAULT_MAX_STRING_LENGTH = 100
DEFAULT_ZERO_COUNT = 0
LIFETIME_SECONDS = 3600
FORMAT = "%Y/%m/%d %H:%M:%S"



class Settings(BaseSettings):
    """
    BaseSettings.

    Позволяет считывать из операционной системы переменные
    окружения, напрямую обращаться к файлу .env.

    Для дефолтных значений используются константы не из env файла.
    """

    app_title: str = 'QRKot'
    description: str = 'Благотворительный фонд поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    min_password_length: int = DEFAULT_MIN_PASSWORD_LENGTH
    min_string_length: int = DEFAULT_MIN_STRING_LENGTH
    max_string_length: int = DEFAULT_MAX_STRING_LENGTH
    zero_count: int = DEFAULT_ZERO_COUNT
    lifetime_seconds: int = LIFETIME_SECONDS
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    admin_email: Optional[str] = None
    format = FORMAT

    class Config:
        """
        Подкласс Config содержит специальный атрибут env_file.

        В нём нужно указать имя файла с переменными окружения;
        полный путь прописывать не обязательно.
        """

        env_file = '.env'


settings = Settings()
