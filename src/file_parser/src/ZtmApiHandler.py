import time

import requests
from requests import Response
from requests.exceptions import Timeout

from ...db.DBLogger import DBLogger
from ...db.FileProcessingLogRepository import FileProcessingLogRepository


class ZtmApiHandler:
    """Handles HTTP requests to ZTM's API.
    Parameters:
    - url - URL of the website to watch
    - waiting_time - waiting time between queries (in seconds)
    - file_processing_log_repository - repository for retrieving logs of processed files
    - db_logger - object for logging messages. If not provided, no messages will be logged.
      regardless if it's actually a new one."""

    HTTP_GET = "GET"
    HTTP_HEAD = "HEAD"

    def __init__(
        self,
        url: str,
        waiting_time: int,
        file_processing_log_repository: FileProcessingLogRepository,
        db_logger: DBLogger = None,
    ) -> None:
        self.url = url
        self.waiting_time = waiting_time
        self.file_processing_log_repository = file_processing_log_repository
        self.db_logger = db_logger
        self._current_filename = None
        self._current_file_hash = None

    def check_if_new_data_available(self, response_file_name: str, response_file_hash: str) -> bool:
        """Checks if new data is available based on the provided HTTP response
        and filename saved from the previous HTTP response."""

        last_successful_log = self.file_processing_log_repository.get_last_successful_log()

        if not last_successful_log:
            return True

        if response_file_name != last_successful_log.file_name:
            return True

        if response_file_hash != last_successful_log.file_contents_hash:
            return True

        return False

    def sleep(self) -> None:
        """Makes the ZtmApiHandler sleep according to it's waiting time."""
        time.sleep(self.waiting_time)

    def send_request(self, method: str) -> Response:
        """Sends the HTTP request using the provided method and returns the response.
        Returns None if the query failed."""
        response = None

        try:
            if method == self.HTTP_HEAD:
                response = requests.head(self.url)
            elif method == self.HTTP_GET:
                response = requests.get(self.url)
            else:
                if self.db_logger:
                    self.db_logger.log_message(
                        f"Invalid method: {method}", __file__, self.db_logger.LOG_TYPE_ERROR
                    )
        except Timeout:
            if self.db_logger:
                self.db_logger.log_message(
                    f"Timeout when trying to query {self.url}",
                    __file__,
                    self.db_logger.LOG_TYPE_ERROR,
                )
        except Exception as e:
            if self.db_logger:
                self.db_logger.log_message(
                    f"Unidentified error when trying to query {self.url}: {e}",
                    __file__,
                    self.db_logger.LOG_TYPE_ERROR,
                )

        return response
