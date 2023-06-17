from sqlalchemy import select

from ...db.DBConnector import DBConnector
from ...db.models import FileProcessingLog


class FileProcessingLogRepository:
    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector

    def get_last_log(self) -> FileProcessingLog | None:
        """Returns the latest record from the file_processing_log table"""

        Session = self.db_connector.sessionmaker

        with Session() as session:
            query = select(FileProcessingLog).order_by(FileProcessingLog.created_at.desc()).limit(1)
            return session.execute(query).scalar_one_or_none()

    def get_last_successful_log(self) -> FileProcessingLog | None:
        """Returns the latest record from the file_processing_log table
        that has processed_successfully set to True"""

        Session = self.db_connector.sessionmaker

        with Session() as session:
            query = (
                select(FileProcessingLog)
                .where(FileProcessingLog.processed_successfully)
                .order_by(FileProcessingLog.created_at.desc())
                .limit(1)
            )
            return session.execute(query).scalar_one_or_none()
