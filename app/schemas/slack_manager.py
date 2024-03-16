from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class SlackConfigData(BaseSettings):
    SLACK_API_URL: str = Field(default="https://slack.com/api/")
    SLACK_LOG_CHANNEL_ID: str = Field(...)
    CHAT_POST_MESSAGE: str = Field(default="chat.postMessage")
    SERVICE_NAME: str = Field(...)
    SLACK_API_BOT_DEV_INFORMER_TOKEN: str = Field(...)
    SLACK_APP_NAME: str = Field(...)
    SLACK_APP_TYPE: str = Field(...)

    @field_validator('SLACK_API_BOT_DEV_INFORMER_TOKEN', 'SLACK_APP_NAME', 'SLACK_APP_TYPE', 'SLACK_LOG_CHANNEL_ID', 'SERVICE_NAME')
    @classmethod
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
