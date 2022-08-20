import logging

from . import sql_db
from .models.Log import Log


class DBLogger:
    def __init__(self):
        self.db = sql_db

    def log_message(self, message, file, type, with_commit=True) -> bool:
        try:
            log = Log(message=message, file=file, type=type)
            self.db.session.add(log)
            if with_commit:
                self.db.session.commit()
            return True
        except Exception as e:
            logging.error("Failed to create a log: %s", e)
            return False
