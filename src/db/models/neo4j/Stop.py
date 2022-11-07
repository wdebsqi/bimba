from typing import Literal

from .Node import Node

LABEL = "Stop"
ID = "stop_id"
NAME = "stop_name"
CODE = "stop_code"
LAT = "stop_lat"
LON = "stop_lon"
ZONE = "zone_id"


class Stop(Node):
    def __init__(
        self, id: int, name: str, code: str, lat: float, lon: float, zone: Literal["A", "B", "C"]
    ):
        super().__init__()
        self.label = LABEL
        self.properties = {
            ID: id,
            NAME: name,
            CODE: code,
            LAT: lat,
            LON: lon,
            ZONE: zone,
        }
