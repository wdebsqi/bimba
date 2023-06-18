from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .Base import CRUD, Base


class FileProcessingLog(Base, CRUD):
    __tablename__ = "file_processing_logs"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    file_name = Column(String, nullable=False)
    file_contents_hash = Column(String, nullable=False)
    processed_successfully = Column(Boolean, nullable=False)

    def __repr__(self):
        return (
            "<FileProcessingLog("
            + f"id={self.id},"
            + f"created_at={self.created_at},"
            + f"file_name={self.file_name},"
            + f"file_contents_hash={self.file_contents_hash},"
            + f"processed_successfully={self.processed_successfully})>"
        )
