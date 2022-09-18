import re
import time

import requests
from requests import Response
from requests.exceptions import Timeout

from ...db.DBLogger import DBLogger


class SiteWatcher:
    """Watches ZTM website for new data and allows for downloading it.
    Parameters:
    - url - URL of the website to watch
    - waiting_time - waiting time between queries (in seconds)
    - db_logger - object for logging messages. If not provided, no messages will be logged.
    - download_initial_file - if True, the watcher will download the file on the first loop,
      regardless if it's actually a new one."""

    HTTP_GET = "GET"
    HTTP_HEAD = "HEAD"
    HEADER_FILENAME_KEY = "Content-Disposition"
    HEADER_FILENAME_INNER_KEY = "filename"
    HEADER_FILENAME_VALUE_REDUNDANT_CHARS = ['"', "="]

    def __init__(
        self,
        url: str,
        waiting_time: int,
        db_logger: DBLogger = None,
        download_initial_file: bool = False,
    ) -> None:
        self.url = url
        self.waiting_time = waiting_time
        self.db_logger = db_logger
        self.download_initial_file = download_initial_file
        self._last_filename = None

    def check_if_new_data_available(self, response: Response) -> bool:
        """Checks if new data is available based on the provided HTTP response
        and filename saved from the previous HTTP response."""

        result = False
        header = self._extract_response_header(response, self.HEADER_FILENAME_KEY)
        new_filename = self._read_filename_from_response_header(header)

        # True in one of two cases:
        # either this is the first loop and Watcher is supposed to download initial file
        # or this is not the first loop and the current filename is different than the previous one
        if (self._last_filename is None and self.download_initial_file) or (
            self._last_filename is not None and self._last_filename != new_filename
        ):
            result = True

        if self._last_filename is not None and self._last_filename != new_filename:
            if self.db_logger:
                self.db_logger.log_message(
                    f"New file available: {new_filename}", __file__, self.db_logger.LOG_TYPE_INFO
                )

        self._last_filename = new_filename
        return result

    def get_current_filename(self) -> str:
        """Returns the current filename."""
        return self._last_filename

    def sleep(self) -> None:
        """Makes the SiteWatcher sleep according to it's waiting time."""
        time.sleep(self.waiting_time)

    def query_site(self, method: str) -> Response:
        """Queries the site using the provided HTTP method and returns the response.
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

    def _extract_response_header(self, response: Response, header: str) -> str:
        """Extracts the right header's value from the HTTP response."""
        return response.headers[header]

    def _read_filename_from_response_header(self, header: str) -> str:
        """Extracts filename from the provided response header."""

        result = header.split(self.HEADER_FILENAME_INNER_KEY)[1]
        if len(result) == 1:
            if self.db_logger:
                self.db_logger.log_message(
                    f"No filename found in the header: {header}",
                    __file__,
                    self.db_logger.LOG_TYPE_ERROR,
                )

        pattern = ""
        for char in self.HEADER_FILENAME_VALUE_REDUNDANT_CHARS:
            pattern += "\\" + char
        pattern = f"[{pattern}]"

        return re.sub(pattern, "", result)
