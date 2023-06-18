import pytest

from ...db.DBConnector import DBConnector
from ...db.DBLogger import DBLogger
from ...db.Neo4jDBController import Neo4jDBController
from .. import create_app
from ..src.LinePicker import LinePicker
from ..src.PathFinder import PathFinder
from ..src.RoutePicker import RoutePicker
from . import NEO4J_PASSWORD, NEO4J_URL, NEO4J_USERNAME


@pytest.fixture(scope="module")
def db_connector():
    return DBConnector()


@pytest.fixture(scope="module")
def db_logger():
    return DBLogger()


@pytest.fixture(scope="module")
def neo4j_db_controller(db_logger):
    controller = Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, db_logger)
    yield controller
    controller.close()


@pytest.fixture(scope="module")
def line_picker():
    return LinePicker()


@pytest.fixture(scope="module")
def path_finder(neo4j_db_controller):
    return PathFinder(neo4j_db_controller)


@pytest.fixture(scope="module")
def route_picker(path_finder, line_picker):
    return RoutePicker(path_finder, line_picker)


@pytest.fixture(scope="module")
def valid_stop_names():
    return ["Rondo Rataje", "Pl. Wielkopolski", "Ogrody", "Półwiejska"]


@pytest.fixture(scope="module")
def invalid_stop_names():
    return ["abcdef", "-1", "null", "bool"]


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.testing = True

    return app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
