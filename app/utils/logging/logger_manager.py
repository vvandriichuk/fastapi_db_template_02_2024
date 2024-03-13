import logging
import http.client as http_client

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

from app.utils.check_otlp_credentials import (
    CertificateCredentialStrategy,
    CredentialStrategy, TokenCredentialStrategy,
)
from app.utils.integrations.slack.slack_integration import SlackLogHandler
from app.config.logger_config import LoggerConfigData
from app.utils.str_to_bool import str_to_bool


class LoggerManager:
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
    environment = LoggerConfigData.ENVIRONMENT()

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._logger = cls.initialize_logger()
        return cls._logger

    @classmethod
    def initialize_logger(cls):
        # Create a logger
        logger = logging.getLogger(cls.logging_name if cls.logging_name else __name__)
        logger.setLevel(cls.logging_level)

        # Read logs from http connections
        if cls.logging_http_client_enable is True:
            http_client.HTTPConnection.debuglevel = 1

        # Console handler
        if cls.logging_console_enable is True:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(cls.logging_level)
            console_formatter = logging.Formatter(cls.logging_formatter)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        # File handler
        if cls.logging_file_enable is True:
            file_handler = logging.FileHandler(cls.logging_file_path)
            file_handler.setLevel(cls.logging_level)
            file_formatter = logging.Formatter(cls.logging_formatter)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        # Slack handler
        if cls.slack_notifications_enable is True:
            slack_handler = SlackLogHandler()
            slack_handler.setLevel(
                logging.ERROR)
            formatter = logging.Formatter(cls.logging_formatter)
            slack_handler.setFormatter(formatter)
            logger.addHandler(slack_handler)

        # OTLP
        if cls.logging_otlp_enable is True:
            resource = Resource.create({"service.name": cls.logging_name,
                                        "deployment.environment": cls.environment})
            logger_provider = LoggerProvider(resource=resource)
            set_logger_provider(logger_provider)

            credentials = None

            if cls.logging_otlp_use_credentials is True:
                credential_strategy: CredentialStrategy

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
            logger.addHandler(otlp_handler)

        return logger
