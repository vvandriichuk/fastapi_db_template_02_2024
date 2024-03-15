from pydantic import Field
from pydantic_settings import BaseSettings


class MetricsConfigData(BaseSettings):
    METRICS_ENABLE: str = Field(default='')
    METRICS_USE_CREDENTIALS: str = Field(default='')
    METRICS_TOKEN: str = Field(default='')
    METRICS_OTLP_ENDPOINT: str = Field(default='')
    METRICS_OTLP_INSECURE: str = Field(default='')
    METRICS_SERVICE_NAME: str = Field(default='')
    METRICS_LIBRARY_NAME: str = Field(default='')
    METRICS_LIBRARY_VERSION: str = Field(default='')
    ENVIRONMENT: str = Field(default='')

    class Config:
        # Read the.env file
        env_file = '.env'
        env_file_encoding = 'utf-8'
