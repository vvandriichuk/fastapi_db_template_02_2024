from loguru import logger
import logging
from pydantic import ValidationError
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
from app.schemas.logger_manager import LoggerConfigData
from app.utils.logging.abc_logger_manager import BaseLoggerManager
from app.utils.str_to_bool import str_to_bool


class LoguruManager(BaseLoggerManager):
    def __init__(self):
        try:
            config = LoggerConfigData()
        except ValidationError as e:
            raise SystemExit(e)

        self.logging_name = config.LOGGING_NAME
        self.logging_level = config.LOGGING_LEVEL
        self.logging_http_client_enable = str_to_bool(config.LOGGING_HTTP_CLIENT_ENABLE)
        self.logging_console_enable = str_to_bool(config.LOGGING_CONSOLE_ENABLE)
        self.logging_formatter = config.LOGGING_FORMATTER
        self.logging_file_enable = str_to_bool(config.LOGGING_FILE_ENABLE)
        self.logging_file_path = config.LOGGING_FILE_PATH
        self.logging_otlp_enable = str_to_bool(config.LOGGING_OTLP_ENABLE)
        self.logging_otlp_endpoint = config.LOGGING_OTLP_ENDPOINT
        self.logging_otlp_insecure = str_to_bool(config.LOGGING_OTLP_INSECURE)
        self.logging_otlp_use_credentials = config.LOGGING_OTLP_USE_CREDENTIALS
        self.use_ssl_certificate = False
        self.ssl_certificate_path = None
        self.token = config.LOGGING_TOKEN
        self.slack_notifications_enable = str_to_bool(config.LOGGING_SLACK_ENABLE)
        self.environment = config.ENVIRONMENT
        self._logger = self.initialize_logger()

    def initialize_logger(self):
        logger.remove()
        resource = Resource.create({"service.name": self.logging_name,
                                    "deployment.environment": self.environment})
        logger_provider = LoggerProvider(resource=resource)
        set_logger_provider(logger_provider)

        if self.logging_console_enable is True:
            logger.add(sys.stdout, level=self.logging_level, format=self.logging_formatter)

        if self.logging_file_enable is True:
            logger.add(self.logging_file_path, level=self.logging_level, format=self.logging_formatter, rotation="10 MB")

        # Slack handler
        if self.slack_notifications_enable is True:
            slack_handler = SlackLogHandler()
            slack_handler.setLevel(
                logging.ERROR)
            formatter = logging.Formatter(self.logging_formatter)
            slack_handler.setFormatter(formatter)
            logger.add(slack_handler)

        if self.logging_otlp_enable is True:
            credentials = None
            if self.logging_otlp_use_credentials is True:
                if self.use_ssl_certificate is True:
                    credential_strategy = CertificateCredentialStrategy(self.ssl_certificate_path)
                else:
                    credential_strategy = TokenCredentialStrategy(self.token)
                credentials = credential_strategy.get_credentials()

            otlp_exporter = OTLPLogExporter(
                endpoint=self.logging_otlp_endpoint,
                insecure=self.logging_otlp_insecure,
                credentials=credentials
            )

            logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
            otlp_handler = LoggingHandler(level=self.logging_level, logger_provider=logger_provider)

            # Attach OTLP handler to root logger
            logger.add(otlp_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self._logger
