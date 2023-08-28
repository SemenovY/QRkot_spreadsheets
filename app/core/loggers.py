"""
Настройка логирования для модуля users.on_after_register
"""
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    f'{__name__}.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
handler = logging.FileHandler(f'{__name__}.log', mode='w')
