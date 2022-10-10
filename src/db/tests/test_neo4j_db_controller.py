from ..Neo4jDBController import Neo4jDBController


def test_ping(neo4j_db_controller):
    assert neo4j_db_controller.ping()


def test_class_inheritance(neo4j_db_controller):
    assert isinstance(neo4j_db_controller, Neo4jDBController)
