import pytest
from neo4j_db.src import neo4j_instance


class TestNeo4j:
    @pytest.fixture(scope="class")
    def neo4j_db(self):
        yield neo4j_instance
        neo4j_instance.close()

    def test_ping(self, neo4j_db):
        assert neo4j_db.ping() is True
