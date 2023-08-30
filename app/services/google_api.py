"""
Функции взаимодействия приложения с Google API
"""
from datetime import datetime, timedelta
from typing import Dict, List

from aiogoogle import Aiogoogle
from app.core.config import settings

ROWCOUNT = 100
COLUMN_COUNT = 11

NOW_DATE_TIME = datetime.now().strftime(settings.format)
SHEETS_VERSION = ('sheets', 'v4')
DRIVE_VERSION = ('drive', 'v3')

SHEET_RANGE = 'A1:E30'
VALUE_INPUT_OPTION = 'USER_ENTERED'

TITLE = 'Лист1'
SHEET_TYPE = 'GRID'
LOCALE = 'ru_RU'

MAJOR_DIMENSION = 'ROWS'
PERMISSIONS_FIELDS = 'id'

USER_TYPE = 'user'
USER_ROLE = 'writer'

SPREAD_SHEET_BODY = {
    'properties': {'title': f'Отчет на {NOW_DATE_TIME}',
                   'locale': LOCALE},
    'sheets': [{'properties': {'sheetType': SHEET_TYPE,
                               'sheetId': settings.zero_count,
                               'title': TITLE,
                               'gridProperties': {
                                   'rowCount': ROWCOUNT,
                                   'columnCount': COLUMN_COUNT
                               }}}
               ]
}

TABLE_VALUES = [
    ['Отчет от', NOW_DATE_TIME],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Функция создания таблицы должна получать на вход экземпляр класса
    Aiogoogle и возвращать строку с ID созданного документа.
    """
    service = await wrapper_services.discover(SHEETS_VERSION)
    spreadsheet_body = SPREAD_SHEET_BODY
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция для предоставления прав доступа вашему личному аккаунту к
    созданному документу (будет называться set_user_permissions()) должна
    принимать строку с ID документа, на который надо дать права доступа,
    и экземпляр класса Aiogoogle.
    """
    permissions_body = {
        'type': USER_TYPE,
        'role': USER_ROLE,
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover(DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields=PERMISSIONS_FIELDS
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List[Dict],
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция будет записывать, полученную из базы данных информацию в
    документ с таблицами.
    В качестве параметров эта функция будет получать ID документа,
    информацию из базы и объект Aiogoogle.
    """
    service = await wrapper_services.discover(SHEETS_VERSION)
    table_values = TABLE_VALUES.copy()

    for project in projects:
        table_values.append(
            (project['name'],
             str(timedelta(project['collection time'])),
             project['description']
             )
        )

    update_body = {
        'majorDimension': MAJOR_DIMENSION,
        'values': table_values
    }

    _ = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=SHEET_RANGE,
            valueInputOption=VALUE_INPUT_OPTION,
            json=update_body
        )
    )
