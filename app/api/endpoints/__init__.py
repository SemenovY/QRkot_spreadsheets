"""
Вообще, в проектах на FastAPI импорты классов через __init__.py —
это частое явление, причем не только в каталогах с моделями или эндпоинтами,
но и в каталогах crud/, schemas/ или в других.
Теперь объекты роутеров будут доступны непосредственно
из пакета app/api/endpoints.
"""
from .user import router as user_router # noqa
from .charity_project import router as charity_project_router # noqa
from .donation import router as donation_router # noqa
