import pytest

from ..DBConnector import DBConnector
from ..DBLogger import DBLogger
from ..Neo4jDBController import Neo4jDBController
from . import NEO4J_PASSWORD, NEO4J_URL, NEO4J_USERNAME


@pytest.fixture(scope="module")
def db_connector():
    return DBConnector()


@pytest.fixture(scope="module")
def logger(db_connector):
    return DBLogger(db_connector)


@pytest.fixture(scope="module")
def neo4j_db_controller(logger):
    return Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, logger)
