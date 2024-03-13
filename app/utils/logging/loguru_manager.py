from loguru import logger
import logging
import sys

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from app.utils.check_otlp_credentials import (
    CertificateCredentialStrategy,
    CredentialStrategy, TokenCredentialStrategy,
)
from app.utils.integrations.slack.slack_integration import SlackLogHandler
from app.config.logger_config import LoggerConfigData
from app.utils.str_to_bool import str_to_bool


class LoguruManager:
    _logger = None
    logging_name = LoggerConfigData.LOGGING_NAME()
    logging_level = LoggerConfigData.LOGGING_LEVEL()
    logging_http_client_enable = str_to_bool(LoggerConfigData.LOGGING_HTTP_CLIENT_ENABLE())
    logging_console_enable = str_to_bool(LoggerConfigData.LOGGING_CONSOLE_ENABLE())
    logging_formatter = LoggerConfigData.LOGGING_FORMATTER()
    logging_file_enable = str_to_bool(LoggerConfigData.LOGGING_FILE_ENABLE())
    logging_file_path = LoggerConfigData.LOGGING_FILE_PATH()
    logging_otlp_enable = str_to_bool(LoggerConfigData.LOGGING_OTLP_ENABLE())
    logging_otlp_endpoint = LoggerConfigData.LOGGING_OTLP_ENDPOINT()
    logging_otlp_insecure = str_to_bool(LoggerConfigData.LOGGING_OTLP_INSECURE())
    logging_otlp_use_credentials = LoggerConfigData.LOGGING_OTLP_USE_CREDENTIALS()
    use_ssl_certificate = False
    ssl_certificate_path = None
    token = LoggerConfigData.LOGGING_TOKEN()
    slack_notifications_enable = str_to_bool(LoggerConfigData.LOGGING_SLACK_ENABLE())

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

        if cls.logging_console_enable is True:
            logger.add(sys.stdout, level=cls.logging_level, format=cls.logging_formatter)

        if cls.logging_file_enable is True:
            logger.add(cls.logging_file_path, level=cls.logging_level, format=cls.logging_formatter, rotation="10 MB")

        # Slack handler
        if cls.slack_notifications_enable is True:
            slack_handler = SlackLogHandler()
            slack_handler.setLevel(
                logging.ERROR)
            formatter = logging.Formatter(cls.logging_formatter)
            slack_handler.setFormatter(formatter)
            logger.add(slack_handler)

        if cls.logging_otlp_enable is True:
            credentials = None
            if cls.logging_otlp_use_credentials is True:
                if cls.use_ssl_certificate is True:
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
