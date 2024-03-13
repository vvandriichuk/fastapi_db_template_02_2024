import os

from app.utils.abstract_custom_str_enum import AbstractCustomStrEnum


class MetricsConfigData(AbstractCustomStrEnum):
    METRICS_ENABLE = os.environ.get('METRICS_ENABLE', '')
    METRICS_USE_CREDENTIALS = os.environ.get('METRICS_USE_CREDENTIALS', '')
    METRICS_TOKEN = os.environ.get('METRICS_TOKEN', '')
    METRICS_OTLP_ENDPOINT = os.environ.get('METRICS_OTLP_ENDPOINT', '')
    METRICS_OTLP_INSECURE = os.environ.get('METRICS_OTLP_INSECURE', '')
    METRICS_SERVICE_NAME = os.environ.get('METRICS_SERVICE_NAME', '')
    METRICS_LIBRARY_NAME = os.environ.get('METRICS_LIBRARY_NAME', '')
    METRICS_LIBRARY_VERSION = os.environ.get('METRICS_LIBRARY_VERSION', '')
    ENVIRONMENT = os.environ.get('ENVIRONMENT', '')
