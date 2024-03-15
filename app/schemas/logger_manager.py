from pydantic import Field
from pydantic_settings import BaseSettings


class LoggerConfigData(BaseSettings):
    LOGGING_NAME: str = Field(default='')
    LOGGING_LEVEL: str = Field(default='INFO')
    LOGGING_HTTP_CLIENT_ENABLE: bool = Field(default=False)
    LOGGING_CONSOLE_ENABLE: bool = Field(default=False)
    LOGGING_FORMATTER: str = Field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    LOGGING_FILE_ENABLE: bool = Field(default=False)
    LOGGING_FILE_PATH: str = Field(default='')
    LOGGING_OTLP_ENABLE: bool = Field(default=False)
    LOGGING_OTLP_ENDPOINT: str = Field(default='')
    LOGGING_OTLP_INSECURE: bool = Field(default=False)
    LOGGING_OTLP_USE_CREDENTIALS: bool = Field(default=False)
    LOGGING_TOKEN: str = Field(default='')
    LOGGING_SLACK_ENABLE: bool = Field(default=False)
    ENVIRONMENT: str = Field(default='')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
