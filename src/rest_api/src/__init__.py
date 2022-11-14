import os

from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger
from ...db.Neo4jDBController import Neo4jDBController
from .LinePicker import LinePicker
from .PathFinder import PathFinder
from .ResponseFormatter import ResponseFormatter
from .RoutePicker import RoutePicker
from .StopsGetter import StopsGetter

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") if os.getenv("NEO4J_PASSWORD") else ""
NEO4J_URL = os.getenv("NEO4J_URL") if os.getenv("NEO4J_URL") else ""
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") if os.getenv("NEO4J_USERNAME") else ""

db_connector = DBConnector()
db_logger = DBLogger(db_connector)
neo4j_controller = Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, db_logger)
line_picker = LinePicker()
path_finder = PathFinder(neo4j_controller)
route_picker = RoutePicker(path_finder, line_picker)
stops_getter = StopsGetter(neo4j_controller)
response_formatter = ResponseFormatter()
