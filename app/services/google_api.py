"""
Функции взаимодействия приложения с Google API
"""
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.models import CharityProject

ROWCOUNT = 100
COLUMNCOUNT = 11


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Функция создания таблицы должна получать на вход экземпляр класса
    Aiogoogle и возвращать строку с ID созданного документа.
    """
    now_date_time = datetime.now().strftime(settings.format)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет на {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': settings.zero_count,
                                   'title': 'Лист1',
                                   'gridProperties': {
                                       'rowCount': ROWCOUNT,
                                       'columnCount': COLUMNCOUNT
                                   }}}
                   ]
    }
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
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        objects: List[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция будет записывать, полученную из базы данных информацию в
    документ с таблицами.
    В качестве параметров эта функция будет получать ID документа,
    информацию из базы и объект Aiogoogle.
    """
    now_date_time = datetime.now().strftime(settings.format)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']

    ]
    # table_values[0].append(now_date_time)
    # table_values = [*table_values,
    #                 *[list(map(str,
    #                            [project.name,
    #                             project.close_date - project.create_date,
    #                             project.description])) for project in
    #                   objects]
    #                 ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }


    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
