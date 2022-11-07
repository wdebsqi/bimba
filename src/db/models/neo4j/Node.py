from abc import ABC

from .Object import Object

TYPE = "node"


class Node(Object, ABC):
    def __init__(self):
        super().__init__()
        self.type = TYPE
