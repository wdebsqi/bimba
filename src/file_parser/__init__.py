import os

from ..db.DBConnector import DBConnector
from ..db.DBLogger import DBLogger
from ..db.FileProcessingLogRepository import FileProcessingLogRepository
from ..db.Neo4jDBController import Neo4jDBController
from .src.ConnectionsParser import ConnectionsParser
from .src.FileProcessor import FileProcessor
from .src.StopsParser import StopsParser
from .src.ZtmApiHandler import ZtmApiHandler

FILE_STOPS = ""  # path to stops.txt file
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") if os.getenv("NEO4J_PASSWORD") else ""
NEO4J_URL = os.getenv("NEO4J_URL") if os.getenv("NEO4J_URL") else ""
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") if os.getenv("NEO4J_USERNAME") else ""
API_HANDLER_WAIT_TIME = 3600
STOP_CODE_COLUMN = "stop_code"
STOP_ID_COLUMN = "stop_id"
STOP_LAT_COLUMN = "stop_lat"
STOP_LON_COLUMN = "stop_lon"
STOP_NAME_COLUMN = "stop_name"
STOP_COLUMNS = ["id", "name", "lat", "lon"]
ZONE_COLUMN = "zone_id"
ZTM_FILES_DIRECTORY = os.getenv("ZTM_FILES_DIRECTORY") if os.getenv("ZTM_FILES_DIRECTORY") else ""
ZTM_FILES_ENDPOINT = "https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile"

db_connector = DBConnector()
db_logger = DBLogger()
neo4j_controller = Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, db_logger)
file_processor = FileProcessor(db_logger)
file_processing_log_repository = FileProcessingLogRepository(db_connector)
stops_parser = StopsParser()
api_handler = ZtmApiHandler(
    ZTM_FILES_ENDPOINT, API_HANDLER_WAIT_TIME, file_processing_log_repository, True
)
connections_parser = ConnectionsParser(db_logger)
