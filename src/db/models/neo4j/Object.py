from abc import ABC


class Object(ABC):
    def __init__(self):
        self.type = None
        self.label = None
        self.properties = None

    def __repr__(self):
        return f"{self.type}:{self.label} {self.properties}"
