from datetime import datetime

from .models.Log import Log


class DBLogger:
    LOG_TYPE_DEBUG = "debug"
    LOG_TYPE_ERROR = "error"
    LOG_TYPE_INFO = "info"
    LOG_TYPE_TEST = "test"

    def log_message(self, message: str, file: str, type: str) -> bool:
        """Logs a message and returns boolean value indicating if the log was successful.
        Parameters:
        - message: message to be logged
        - file: the information about the file related to the log (e.g. __file__)
        - type: the type of log. Use the LOG_TYPE_* constants"""
        try:
            log = Log(created_at=datetime.now(), message=message, file=file, type=type)
            log.save()
            return True
        except Exception as e:
            print(f"Error {e} encountered when logging message {message}")
            return False
