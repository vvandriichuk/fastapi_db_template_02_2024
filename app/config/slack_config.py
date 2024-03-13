from app.utils.abstract_custom_str_enum import AbstractCustomStrEnum


class SlackAPIData(AbstractCustomStrEnum):
    SLACK_API_URL = "https://slack.com/api/"
    LOG_CHANNEL_ID = "C06NXKYSGSE"
    CHAT_POST_MESSAGE = "chat.postMessage"
    FILES_UPLOAD = "files.upload"
