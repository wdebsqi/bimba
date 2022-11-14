from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String

from .Base import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    ip = Column(String, nullable=False)
    uri = Column(String, nullable=False)
    method = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    form_data = Column(JSON, nullable=False)
