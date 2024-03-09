from loguru import logger
import sys
import os

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from app.utils.check_otlp_credentials import (
    CertificateCredentialStrategy,
    CredentialStrategy, TokenCredentialStrategy,
)


class LoguruManager:
    _logger = None
    logging_name = os.environ.get('LOGGING_NAME', '')
    logging_level = os.environ.get('LOGGING_LEVEL', 'INFO').upper()
    logging_console_enable = os.environ.get('LOGGING_CONSOLE_ENABLE', 'False')
    logging_formatter = os.environ.get('LOGGING_FORMATTER', '{time} - {name} - {level} - {message}')
    logging_file_enable = os.environ.get('LOGGING_FILE_ENABLE', 'False')
    logging_file_path = os.environ.get('LOGGING_FILE_PATH', '')
    logging_otlp_enable = os.environ.get('LOGGING_OTLP_ENABLE', 'False')
    logging_otlp_endpoint = os.environ.get('LOGGING_OTLP_ENDPOINT', '')
    logging_otlp_insecure = os.environ.get('LOGGING_OTLP_INSECURE', 'False')
    logging_otlp_use_credentials = os.environ.get('LOGGING_OTLP_USE_CREDENTIALS', 'False')
    use_ssl_certificate = False
    ssl_certificate_path = None
    token = os.environ.get('LOGGING_TOKEN', '')

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = cls.initialize_logger()
        return cls._logger

    @classmethod
    def initialize_logger(cls):
        logger.remove()
        resource = Resource.create({"service.name": cls.logging_name})
        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)

        if cls.logging_console_enable:
            logger.add(sys.stdout, level=cls.logging_level, format=cls.logging_formatter)

        if cls.logging_file_enable:
            logger.add(cls.logging_file_path, level=cls.logging_level, format=cls.logging_formatter, rotation="10 MB")

        if cls.logging_otlp_enable:
            resource = Resource.create({"service.name": cls.logging_name})

            credentials = None
            if cls.logging_otlp_use_credentials:
                if cls.use_ssl_certificate:
                    credential_strategy = CertificateCredentialStrategy(cls.ssl_certificate_path)
                else:
                    credential_strategy = TokenCredentialStrategy(cls.token)
                credentials = credential_strategy.get_credentials()

            otlp_exporter = OTLPLogExporter(
                endpoint=cls.logging_otlp_endpoint,
                insecure=cls.logging_otlp_insecure,
                credentials=credentials
            )

            logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
            otlp_handler = LoggingHandler(level=cls.logging_level, logger_provider=logger_provider)

            # Attach OTLP handler to root logger
            logger.add(otlp_handler)

        return logger
