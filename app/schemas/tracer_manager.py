from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class TraceConfigData(BaseSettings):
    TRACE_SERVICE_NAME: str = Field(default='', description="The name of the service for which tracing is enabled.")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(default='', description="The endpoint for sending traces.")
    TRACE_INSECURE: bool = Field(default=True,
                           description="Flag to specify if the connection should be insecure (not use TLS).")
    TRACE_USE_CREDENTIALS: bool = Field(default=False,
                                  description="Flag to determine if credentials are required for trace exporting.")
    USE_SSL_CERTIFICATE: bool = Field(default=False,
                                      description="Flag to determine if an SSL certificate is used for a secure "
                                                  "connection.")
    SSL_CERTIFICATE_PATH: Optional[str] = Field(default=None,
                                                description="The path to the SSL certificate if USE_SSL_CERTIFICATE "
                                                            "is set to True.")
    TRACE_TOKEN: str = Field(default='',
                       description="The token used for authentication when exporting traces, if USE_CREDENTIALS is "
                                   "set to True.")
    ENVIRONMENT: str = Field(default='',
                             description="The deployment environment where the application is running, such as "
                                         "'production', 'development', or 'staging'.")
    TRACE_SAMPLE_RATE: float = Field(default=1 / 100, description="The sampling rate for collecting traces.")

    @staticmethod
    @field_validator('OTEL_EXPORTER_OTLP_ENDPOINT', 'TRACE_SERVICE_NAME', 'ENVIRONMENT')
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
