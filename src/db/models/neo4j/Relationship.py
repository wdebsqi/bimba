from abc import ABC

from .Object import Object

TYPE = "relationship"


class Relationship(Object, ABC):
    def __init__(self):
        super().__init__()
        self.type = TYPE
