from neo4j_db import neo4j_db


class TestNeo4j:
    def test_ping(self):
        assert neo4j_db.ping() is True
