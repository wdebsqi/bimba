import re
from zipfile import ZipFile

import pandas as pd
import requests

from ...db.DBLogger import DBLogger


class FileProcessor:
    """Handles processing files from ZTM. Example operations include:
    - unzipping file archive
    - filtering files on a given column
    - removing selected columns from the files
    - setting new column names

    Parameters:
    - db_logger - object for logging messages. If not provided, no messages will be logged."""

    HEADER_FILENAME_KEY = "Content-Disposition"
    HEADER_FILENAME_INNER_KEY = "filename"
    HEADER_FILENAME_VALUE_REDUNDANT_CHARS = ['"', "="]

    def __init__(self, db_logger: DBLogger = None):
        self.db_logger = db_logger

    def download_zip_file(self, response: requests.Response, destination_path: str) -> bool:
        """Downloads the .zip file from the given URL and saves in in the provided destination."""
        try:
            with open(destination_path, "wb") as file:
                file.write(response.content)
            if self.db_logger:
                self.db_logger.log_message(
                    f"Successfully downloaded file to {destination_path}",
                    __file__,
                    self.db_logger.LOG_TYPE_INFO,
                )
            return True
        except Exception as e:
            if hasattr(e, "message"):
                if self.db_logger:
                    self.db_logger.log_message(e.message, __file__, self.db_logger.LOG_TYPE_ERROR)
            else:
                if self.db_logger:
                    self.db_logger.log_message(str(e), __file__, self.db_logger.LOG_TYPE_ERROR)
            return False

    def unzip_file_archive(
        self, archive_file_path: str, destination_path: str, files_to_extract: list = None
    ) -> bool:
        """Opens file archive provided by ZTM and unpacks the files to the provided directory.
        The files to extract can be specified using files_to_extract parameter.
        If the list is not provided, all files in the archive will be extracted."""
        try:
            with ZipFile(archive_file_path, "r") as zip_file:
                zip_file.extractall(destination_path, files_to_extract)
            if self.db_logger:
                self.db_logger.log_message(
                    f"Successfully unzipped files {files_to_extract} to {destination_path}",
                    __file__,
                    self.db_logger.LOG_TYPE_INFO,
                )
            return True
        except Exception as e:
            if hasattr(e, "message"):
                if self.db_logger:
                    self.db_logger.log_message(e.message, __file__, self.db_logger.LOG_TYPE_ERROR)
            else:
                if self.db_logger:
                    self.db_logger.log_message(str(e), __file__, self.db_logger.LOG_TYPE_ERROR)
            return False

    def filter_on_column(
        self, df: pd.DataFrame, col_name: str, col_value: str | int | float | bool
    ) -> pd.DataFrame:
        """Filters the provided DataFrame so that only the rows
        with the provided column value are included."""
        return df[df[col_name] == col_value]

    def remove_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Removes chosen columns from the provided DataFrame."""
        return df.drop(columns, axis=1)

    def set_columns(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Sets new column names in the provided DataFrame."""
        df_copy = df.copy()
        df_copy.columns = columns
        return df_copy

    def read_filename_from_response_header(self, response: requests.Response) -> str:
        """Extracts filename from the provided HTTP response's header."""

        header = self._extract_response_header(response, self.HEADER_FILENAME_KEY)
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

    def _extract_response_header(self, response: requests.Response, header: str) -> str:
        """Extracts the right header's value from the HTTP response."""
        return response.headers[header]
