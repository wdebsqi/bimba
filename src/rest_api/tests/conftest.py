import pytest

from ...db.DBLogger import DBLogger
from ...db.Neo4jDBController import Neo4jDBController
from .. import create_app
from ..src.LinePicker import LinePicker
from ..src.PathFinder import PathFinder
from ..src.RoutePicker import RoutePicker
from . import NEO4J_PASSWORD, NEO4J_URL, NEO4J_USERNAME


def _db_logger():
    return DBLogger()


def _neo4j_db_controller():
    return Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, _db_logger())


def _line_picker():
    return LinePicker()


def _path_finder():
    return PathFinder(_neo4j_db_controller(), _db_logger())


@pytest.fixture(scope="module")
def db_logger():
    return _db_logger()


@pytest.fixture(scope="module")
def neo4j_db_controller():
    return _neo4j_db_controller


@pytest.fixture(scope="module")
def line_picker():
    return _line_picker()


@pytest.fixture(scope="module")
def path_finder():
    return _path_finder()


@pytest.fixture(scope="module")
def route_picker():
    return RoutePicker(_path_finder(), _line_picker())


@pytest.fixture(scope="module")
def valid_stop_names():
    return ["Rondo Rataje", "Pl. Wielkopolski", "Ogrody", "Półwiejska"]


@pytest.fixture(scope="module")
def invalid_stop_names():
    return ["abcdef", "-1", "null", "bool"]


@pytest.fixture(scope="module")
def client():
    return create_app().test_client()
