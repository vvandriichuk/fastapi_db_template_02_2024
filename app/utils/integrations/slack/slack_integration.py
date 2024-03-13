import asyncio
import os
import io
import re
import logging

import httpx

from app.config.slack_config import SlackAPIData
from app.utils.get_url_endpoint import get_url


class SlackLogHandler(logging.Handler):
    def emit(self, record):
        try:
            message = self.format(record)
            from app.config.logger_setup import logger
            asyncio.create_task(slack_connector.send_message(message))
        except Exception:
            self.handleError(record)


class SlackConnector:
    def __init__(self) -> None:
        self._request_base_url = SlackAPIData.SLACK_API_URL()
        self._service_name = SlackAPIData.FILES_UPLOAD()
        self._channel_id = SlackAPIData.LOG_CHANNEL_ID()
        self._token = os.environ.get("SLACK_API_BOT_DEV_INFORMER_TOKEN", "")
        self._app_name = os.environ.get("SLACK_APP_NAME", "")
        self._app_type = os.environ.get("SLACK_APP_TYPE", "")

    def _generate_logger_filename_from_record(self, log_record: str) -> str:
        # log_record = 2023-10-09 23:15:05.916 | ERROR    | __main__:main:50 - This error message will be sent to Slack as a file
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \| (\w+)",
            log_record,
        )

        if match:
            timestamp, level = match.groups()

            timestamp = (
                timestamp.replace(" ", "-").replace(":", "-").replace(".", "-")
            )

            filename = f"{self._app_name}_{self._app_type}_{level}_{timestamp}.txt"
            return filename
        else:
            return "Invalid_log_format.txt"

    async def send_message(self, message: str) -> None:
        service_url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        data = {
            "channel": self._channel_id,
            "text": message,
        }

        async with httpx.AsyncClient() as client:
            for _ in range(3):
                try:
                    from app.config.logger_setup import logger
                    response = await client.post(service_url, json=data, headers=headers)
                    logger.info(f"data to Slack: {data}")
                    logger.info(f"response from Slack: {response.text}")
                    response.raise_for_status()
                except BaseException:
                    await asyncio.sleep(1)
                else:
                    break

    async def send_logger_record_as_file(self, record: str) -> None:
        text_bytes = record.encode()
        buffer = io.BytesIO(text_bytes)
        log_filename = self._generate_logger_filename_from_record(record)
        buffer.name = log_filename

        headers = {
            "Authorization": f"Bearer {self._token}",
        }

        files = {
            "file": (log_filename, buffer, "text/plain"),
        }

        data = {
            "channels": self._channel_id,
        }

        async with httpx.AsyncClient() as client:
            for _ in range(3):
                try:
                    response = await client.post(
                        get_url(self._request_base_url, self._service_name),
                        headers=headers,
                        files=files,
                        data=data,
                    )
                    response.raise_for_status()
                except BaseException:
                    await asyncio.sleep(1)
                else:
                    break


slack_connector = SlackConnector()
