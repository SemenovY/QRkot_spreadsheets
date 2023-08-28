"""
Прежде чем работать с пакетом, интерпретатор считывает содержимое
файла __init__.py. Этим можно воспользоваться: в файле __init__.py
«сообщим» интерпрертатору о модели Reservation до того, как он приступит
к выполнению кода.
"""
from .charity_project import CharityProject # noqa
from .user import User # noqa
from .donation import Donation # noqa
