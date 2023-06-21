from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .Base import CRUD, Base


class Log(Base, CRUD):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    type = Column(String, nullable=False)
    file = Column(String, nullable=False)
    message = Column(String, nullable=False)
