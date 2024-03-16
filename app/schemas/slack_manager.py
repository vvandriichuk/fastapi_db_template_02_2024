from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class SlackConfigData(BaseSettings):
    SLACK_API_URL: str = Field(default="https://slack.com/api/",
                               description="The base URL for the Slack API. Default is set to Slack's standard API URL.")
    SLACK_LOG_CHANNEL_ID: str = Field(...,
                                      description="The ID of the Slack channel where logs will be sent. This field is "
                                                  "required.")
    CHAT_POST_MESSAGE: str = Field(default="chat.postMessage",
                                   description="The Slack API method for posting messages to a channel. Default is "
                                               "set to 'chat.postMessage'.")
    SERVICE_NAME: str = Field(...,
                              description="The name of the service integrating with Slack. This could be used to "
                                          "identify the source of the messages in Slack.")
    SLACK_API_BOT_DEV_INFORMER_TOKEN: str = Field(...,
                                                  description="The authentication token for the Slack bot. This token "
                                                              "is used to authorize API calls to Slack.")
    SLACK_APP_NAME: str = Field(...,
                                description="The name of the Slack app. Used for logging and identification purposes "
                                            "within your application or logs.")
    SLACK_APP_TYPE: str = Field(...,
                                description="The type of the Slack app, which could indicate its purpose or the "
                                            "nature of its functionality.")

    @staticmethod
    @field_validator('SLACK_API_BOT_DEV_INFORMER_TOKEN', 'SLACK_APP_NAME', 'SLACK_APP_TYPE', 'SLACK_LOG_CHANNEL_ID', 'SERVICE_NAME')
    def check_not_empty(cls, value, field):
        if not value.strip():
            raise ValueError(f"{field.name} must not be empty")
        return value

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
