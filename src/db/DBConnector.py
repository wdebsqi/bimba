import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnector:
    def __init__(self):
        self.engine = create_engine(os.getenv("POSTGRES_URL").replace("\\", ""))
        self.sessionmaker = sessionmaker(self.engine)
