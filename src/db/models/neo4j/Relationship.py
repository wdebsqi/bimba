from abc import ABC

from .Node import Node
from .Object import Object

TYPE = "relationship"


class Relationship(Object, ABC):
    def __init__(self, from_node: Node, to_node: Node):
        super().__init__()
        self.type = TYPE
        self.from_node = from_node
        self.to_node = to_node
