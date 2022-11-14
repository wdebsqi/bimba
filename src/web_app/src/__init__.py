from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger

db_connector = DBConnector()
db_logger = DBLogger(db_connector)
