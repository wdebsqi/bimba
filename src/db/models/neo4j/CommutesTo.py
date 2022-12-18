from .Relationship import Relationship
from .Stop import ID as STOP_ID
from .Stop import NAME as STOP_NAME
from .Stop import Stop

LABEL = "COMMUTES_TO"
LINES = "lines"


class CommutesTo(Relationship):
    def __init__(self, from_node: Stop, to_node: Stop, lines: list):
        super().__init__(from_node, to_node)
        self.label = LABEL
        self.properties = {LINES: lines}

    def __repr__(self):
        return (
            f"({self.from_node.properties[STOP_ID]}, {self.from_node.properties[STOP_NAME]})"
            + f"-[:{self.label}]->"
            + f"({self.to_node.properties[STOP_ID]}, {self.to_node.properties[STOP_NAME]})"
        )
