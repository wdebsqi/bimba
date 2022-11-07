from .Relationship import Relationship
from .Stop import ID as STOP_ID
from .Stop import NAME as STOP_NAME
from .Stop import Stop

LABEL = "COMMUTES_TO"
LINES = "lines"


class CommutesTo(Relationship):
    def __init__(self, from_stop: Stop, lines: list, to_stop: Stop):
        super().__init__()
        self.label = LABEL
        self.properties = {LINES: lines}
        self.from_stop = from_stop
        self.to_stop = to_stop

    def __repr__(self):
        return (
            f"({self.from_stop.properties[STOP_ID]}, {self.from_stop.properties[STOP_NAME]})"
            + f"-[:{self.label}]->"
            + f"({self.to_stop.properties[STOP_ID]}, {self.to_stop.properties[STOP_NAME]})"
        )
