from pydantic import Field
from pydantic_settings import BaseSettings


class SlackConfigData(BaseSettings):
    SLACK_API_URL: str = Field(default="https://slack.com/api/")
    LOG_CHANNEL_ID: str = Field(default="C06NXKYSGSE")
    CHAT_POST_MESSAGE: str = Field(default="chat.postMessage")
    FILES_UPLOAD: str = Field(default="files.upload")

    class Config:
        # Read the.env file
        env_file = '.env'
        env_file_encoding = 'utf-8'
