from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class MetricsConfigData(BaseSettings):
    METRICS_ENABLE: bool = Field(default=False,
                                 description="Flag to enable or disable the metrics collection feature. When set to "
                                             "True, metrics collection will be active.")
    METRICS_USE_CREDENTIALS: bool = Field(default=False,
                                          description="Flag to determine if credentials are required for metrics "
                                                      "exporting. When True, credentials specified in METRICS_TOKEN "
                                                      "will be used.")
    METRICS_TOKEN: str = Field(default='',
                               description="The token used for authentication when exporting metrics, "
                                           "if METRICS_USE_CREDENTIALS is set to True.")
    METRICS_OTLP_ENDPOINT: str = Field(...,
                                       description="The endpoint for the OpenTelemetry Protocol (OTLP) exporter to "
                                                   "send metrics. This field is required if metrics collection is "
                                                   "enabled.")
    METRICS_OTLP_INSECURE: bool = Field(default=False,
                                        description="Flag to specify if the connection to the OTLP endpoint should be "
                                                    "insecure (not use TLS). Default is False, indicating that a "
                                                    "secure connection is preferred.")
    METRICS_SERVICE_NAME: str = Field(...,
                                      description="The name of the service for which metrics are being collected. "
                                                  "This value is used to identify the source of the metrics.")
    METRICS_LIBRARY_NAME: str = Field(...,
                                      description="The name of the library or application that is generating the "
                                                  "metrics. This helps in categorizing and filtering metrics in the "
                                                  "monitoring system.")
    METRICS_LIBRARY_VERSION: str = Field(...,
                                         description="The version of the library or application that is generating "
                                                     "the metrics. Useful for tracking metrics across different "
                                                     "versions of the software.")
    ENVIRONMENT: str = Field(...,
                             description="The deployment environment where the application is running, such as "
                                         "'production', 'development', or 'staging'. Used to segregate metrics from "
                                         "different environments.")

    @staticmethod
    @field_validator('METRICS_OTLP_ENDPOINT', 'METRICS_SERVICE_NAME', 'METRICS_LIBRARY_NAME', 'METRICS_LIBRARY_VERSION')
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
