from ...db.models.neo4j.CommutesTo import CommutesTo
from ...db.models.neo4j.Node import Node
from ...db.models.neo4j.Object import Object
from ...db.models.neo4j.Relationship import Relationship
from ...db.models.neo4j.Stop import Stop


class TestDbModels:
    def test_class_inheritance(self):
        assert issubclass(Node, Object)
        assert issubclass(Relationship, Object)
        assert issubclass(CommutesTo, Relationship)
        assert issubclass(Stop, Node)
