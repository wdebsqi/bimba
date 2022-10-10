from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()  # used for SQLAlchemy object initialization
Base = declarative_base(metadata=metadata)  # every db table model should inherit from this class
