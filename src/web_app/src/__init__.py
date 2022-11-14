from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger
from .RequestLogger import RequestLogger

db_connector = DBConnector()
db_logger = DBLogger(db_connector)
request_logger = RequestLogger(db_connector, db_logger)
