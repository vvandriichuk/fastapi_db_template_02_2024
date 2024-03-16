from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class MetricsConfigData(BaseSettings):
    METRICS_ENABLE: bool = Field(default=False)
    METRICS_USE_CREDENTIALS: bool = Field(default=False)
    METRICS_TOKEN: str = Field(default='')
    METRICS_OTLP_ENDPOINT: str = Field(...)
    METRICS_OTLP_INSECURE: bool = Field(default=False)
    METRICS_SERVICE_NAME: str = Field(...)
    METRICS_LIBRARY_NAME: str = Field(...)
    METRICS_LIBRARY_VERSION: str = Field(...)
    ENVIRONMENT: str = Field(...)

    @field_validator('METRICS_OTLP_ENDPOINT', 'METRICS_SERVICE_NAME', 'METRICS_LIBRARY_NAME', 'METRICS_LIBRARY_VERSION')
    @classmethod
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
