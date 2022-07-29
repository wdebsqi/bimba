import pytest
from neo4j_db import NEO4J_USERNAME, NEO4J_URL, NEO4J_PASSWORD
from neo4j_db.Neo4jDB import Neo4jDB


class TestNeo4j:
    @pytest.fixture(scope="class")
    def neo4j_db(self):
        db = Neo4jDB(NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD)
        yield db
        db.close()

    def test_ping(self, neo4j_db):
        assert neo4j_db.ping() is True
