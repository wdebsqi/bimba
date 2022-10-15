import os

from ...db.DBLogger import DBLogger
from ...db.Neo4jDBController import Neo4jDBController
from .LinePicker import LinePicker
from .PathFinder import PathFinder
from .ResponseFormatter import ResponseFormatter
from .RoutePicker import RoutePicker

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") if os.getenv("NEO4J_PASSWORD") else ""
NEO4J_URL = os.getenv("NEO4J_URL") if os.getenv("NEO4J_URL") else ""
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME") if os.getenv("NEO4J_USERNAME") else ""

db_logger = DBLogger()
neo4j_controller = Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, db_logger)
line_picker = LinePicker()
path_finder = PathFinder(neo4j_controller, db_logger)
route_picker = RoutePicker(path_finder, line_picker)
response_formatter = ResponseFormatter()
