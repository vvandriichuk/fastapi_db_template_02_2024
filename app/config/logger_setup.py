import os

from app.utils.logging.logger_manager import LoggerManager
from app.utils.logging.loguru_manager import LoguruManager

if os.environ.get('LOGGING_NAME', '') == 'loguru':
    LoguruManager.initialize_logger()
    logger = LoguruManager.get_logger()
else:
    logger = LoggerManager.get_logger()
