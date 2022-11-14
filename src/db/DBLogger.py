from datetime import datetime

from .DBConnector import DBConnector
from .models.Log import Log


class DBLogger:
    LOG_TYPE_DEBUG = "debug"
    LOG_TYPE_ERROR = "error"
    LOG_TYPE_INFO = "info"
    LOG_TYPE_TEST = "test"

    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def log_message(self, message, file, type, with_commit=True) -> bool:
        """Logs a message and returns boolean value indicating if the log was successful.
        Parameters:
        - message: message to be logged
        - file: the information about the file related to the log (e.g. __file__)
        - type: the type of log. Use the LOG_TYPE_* constants
        - with_commit: if True, the log will be commited to the database.
          If False, the log will be added to the session but not commited."""
        try:
            Session = self.db_connector.sessionmaker

            with Session() as session:
                log = Log(created_at=datetime.now(), message=message, file=file, type=type)
                session.add(log)
                if with_commit:
                    session.commit()
                return True
        except Exception as e:
            print(f"Error {e} encountered when logging message {message}")
            return False
