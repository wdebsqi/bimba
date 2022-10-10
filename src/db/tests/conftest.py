import pytest

from ..DBLogger import DBLogger
from ..Neo4jDBController import Neo4jDBController
from . import NEO4J_PASSWORD, NEO4J_URL, NEO4J_USERNAME


@pytest.fixture(scope="module")
def logger():
    return DBLogger()


@pytest.fixture(scope="module")
def neo4j_db_controller():
    return Neo4jDBController(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD, DBLogger())
