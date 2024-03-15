from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import Any


class LoggerConfigData(BaseSettings):
    LOGGING_NAME: str = Field(...)
    LOGGING_LEVEL: str = Field(default='INFO')
    LOGGING_HTTP_CLIENT_ENABLE: bool = Field(default=False)
    LOGGING_CONSOLE_ENABLE: bool = Field(default=False)
    LOGGING_FORMATTER: str = Field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOGGING_FILE_ENABLE: bool = Field(default=False)
    LOGGING_FILE_PATH: str = Field(default='')
    LOGGING_OTLP_ENABLE: bool = Field(default=False)
    LOGGING_OTLP_ENDPOINT: str = Field(...)
    LOGGING_OTLP_INSECURE: bool = Field(default=False)
    LOGGING_OTLP_USE_CREDENTIALS: bool = Field(default=False)
    LOGGING_TOKEN: str = Field(default='')
    LOGGING_SLACK_ENABLE: bool = Field(default=False)
    ENVIRONMENT: str = Field(...)

    @field_validator('LOGGING_NAME', 'LOGGING_OTLP_ENDPOINT', 'ENVIRONMENT')
    @classmethod
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
