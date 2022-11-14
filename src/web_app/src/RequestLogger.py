import os
from datetime import datetime

from flask import Request as FlaskRequest

from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger
from ...db.models import Request


class RequestLogger:
    def __init__(self, db_connector: DBConnector, db_Logger: DBLogger) -> None:
        self.db_connector = db_connector
        self.db_Logger = db_Logger

    def log_request(self, request: FlaskRequest, with_commit=True) -> bool:
        try:
            # skipping logging requests in case the app is running on dev environment
            if not os.getenv("HOST"):
                return True

            Session = self.db_connector.sessionmaker

            with Session() as session:
                method = request.method
                uri = self._remove_host_from_url(request.url)
                ip = request.remote_addr
                form_data = request.form
                user_agent = request.headers.get("User-Agent", None)

                request_to_log = Request(
                    created_at=datetime.now(),
                    ip=ip,
                    uri=uri,
                    method=method,
                    user_agent=user_agent,
                    form_data=form_data,
                )

                session.add(request_to_log)
                if with_commit:
                    session.commit()

                return True

        except Exception as e:
            self.db_Logger.log_message(
                f"Unidentified error when logging user's request: {e}",
                __file__,
                self.db_Logger.LOG_TYPE_ERROR,
            )
            return False

    def _remove_host_from_url(self, url: str) -> str:
        slash_char = "/"
        return slash_char + slash_char.join(url.split(slash_char)[3:])
