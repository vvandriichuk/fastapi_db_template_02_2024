from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class LoggerConfigData(BaseSettings):
    LOGGING_NAME: str = Field(...,
                              description="The unique name for the logger instance, used for identifying logs from "
                                          "this specific source.")
    LOGGING_LEVEL: str = Field(default='INFO',
                               description="The logging level to capture. Defaults to 'INFO'. Supported levels "
                                           "include DEBUG, INFO, WARNING, ERROR, CRITICAL.")
    LOGGING_HTTP_CLIENT_ENABLE: bool = Field(default=False,
                                             description="Flag to enable logging of HTTP client requests and "
                                                         "responses. When True, all HTTP interactions will be logged.")
    LOGGING_CONSOLE_ENABLE: bool = Field(default=False,
                                         description="Flag to enable console logging. When True, logs will be output "
                                                     "to the standard output stream.")
    LOGGING_FORMATTER: str = Field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                   description="The format for log messages. Supports standard formatting strings "
                                               "used by the logging module.")
    LOGGING_FILE_ENABLE: bool = Field(default=False,
                                      description="Flag to enable logging to a file. When True, logs will be written "
                                                  "to the file specified in LOGGING_FILE_PATH.")
    LOGGING_FILE_PATH: str = Field(default='',
                                   description="The path to the log file. Used only if LOGGING_FILE_ENABLE is True.")
    LOGGING_OTLP_ENABLE: bool = Field(default=False,
                                      description="Flag to enable exporting logs via OTLP. When True, logs will be "
                                                  "sent to the OTLP endpoint specified in LOGGING_OTLP_ENDPOINT.")
    LOGGING_OTLP_ENDPOINT: str = Field(...,
                                       description="The endpoint for sending logs via OTLP. Used only if "
                                                   "LOGGING_OTLP_ENABLE is True.")
    LOGGING_OTLP_INSECURE: bool = Field(default=False,
                                        description="Flag for using an insecure connection when sending logs via "
                                                    "OTLP. When True, the connection will not use TLS.")
    LOGGING_OTLP_USE_CREDENTIALS: bool = Field(default=False,
                                               description="Flag for using authentication when sending logs via OTLP. "
                                                           "Requires setting up the appropriate credentials strategy "
                                                           "in the code.")
    LOGGING_TOKEN: str = Field(default='',
                               description="The authentication token used when sending logs via OTLP, "
                                           "if LOGGING_OTLP_USE_CREDENTIALS is True.")
    LOGGING_SLACK_ENABLE: bool = Field(default=False,
                                       description="Flag to enable sending logs to Slack. When True, logs at the "
                                                   "ERROR level will be sent to the specified Slack channel.")
    ENVIRONMENT: str = Field(...,
                             description="The name of the environment in which the application is running. Used for "
                                         "tagging logs.")

    @staticmethod
    @field_validator('LOGGING_NAME', 'LOGGING_OTLP_ENDPOINT', 'ENVIRONMENT')
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
