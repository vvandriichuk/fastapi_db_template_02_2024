import os

from app.utils.logging.abc_logger_manager import BaseLoggerManager
from app.utils.logging.logger_manager import LoggerManager
from app.utils.logging.loguru_manager import LoguruManager

logger_manager: BaseLoggerManager

if os.environ.get('LOGGING_NAME', '') == 'loguru':
    logger_manager = LoguruManager()
else:
    logger_manager = LoggerManager()
