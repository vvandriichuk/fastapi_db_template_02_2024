import os

from app.utils.abstract_custom_str_enum import AbstractCustomStrEnum


class LoggerConfigData(AbstractCustomStrEnum):
    LOGGING_NAME = os.environ.get('LOGGING_NAME', '')
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
    LOGGING_HTTP_CLIENT_ENABLE = os.environ.get('LOGGING_HTTP_CLIENT_ENABLE', 'False')
    LOGGING_CONSOLE_ENABLE = os.environ.get('LOGGING_CONSOLE_ENABLE', 'False')
    LOGGING_FORMATTER = os.environ.get('LOGGING_FORMATTER', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOGGING_FILE_ENABLE = os.environ.get('LOGGING_FILE_ENABLE', 'False')
    LOGGING_FILE_PATH = os.environ.get('LOGGING_FILE_PATH', '')
    LOGGING_OTLP_ENABLE = os.environ.get('LOGGING_OTLP_ENABLE', 'False')
    LOGGING_OTLP_ENDPOINT = os.environ.get('LOGGING_OTLP_ENDPOINT', '')
    LOGGING_OTLP_INSECURE = os.environ.get('LOGGING_OTLP_INSECURE', 'False')
    LOGGING_OTLP_USE_CREDENTIALS = os.environ.get('LOGGING_OTLP_USE_CREDENTIALS', 'False')
    LOGGING_TOKEN = os.environ.get('LOGGING_TOKEN', '')
    LOGGING_SLACK_ENABLE = os.environ.get('LOGGING_SLACK_ENABLE', 'False')
