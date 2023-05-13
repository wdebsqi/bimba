import pandas as pd
import pytest

from ..src.ConnectionsParser import (
    COL_ROUTE_ID,
    COL_STOP_ID,
    COL_STOP_SEQUENCE,
    COL_TRIP_ID,
    RESULT_COL_FROM_STOP,
    RESULT_COL_LINES,
    RESULT_COL_TO_STOP,
    ConnectionsParser,
)
from ..src.FileParser import FileParser
from ..src.SiteWatcher import SiteWatcher
from ..src.StopsParser import StopsParser

COL_ARRIVAL_TIME = "arrival_time"
COL_BRIGADE = "brigade"
COL_DEPARTURE_TIME = "departure_time"
COL_DIRECTION_ID = "direction_id"
COL_DROP_OFF_TYPE = "drop_off_type"
COL_PICKUP_TYPE = "pickup_type"
COL_SERVICE_ID = "service_id"
COL_SHAPE_ID = "shape_id"
COL_STOP_CODE = "stop_code"
COL_STOP_HEADSIGN = "stop_headsign"
COL_STOP_NAME = "stop_name"
COL_STOP_LAT = "stop_lat"
COL_STOP_LON = "stop_lon"
COL_TRIP_HEADSIGN = "trip_headsign"
COL_WHEELCHAIR_ACCESSIBLE = "wheelchair_accessible"
COL_ZONE_ID = "zone_id"


@pytest.fixture(scope="module")
def abstract_parser():
    return FileParser


# StopsParser configuration


@pytest.fixture(scope="module")
def stops_parser():
    return StopsParser()


@pytest.fixture(scope="module")
def example_raw_stops_dataframe():
    data = {
        COL_STOP_ID: [1234, 5678, 9012],
        COL_STOP_CODE: ["ABC1234", "DEF5678", "GHI9012"],
        COL_STOP_NAME: ["ABC", "DEF", "GHI"],
        COL_STOP_LAT: [1.2, 2.3, 3.4],
        COL_STOP_LON: [9.8, 8.7, 7.6],
        COL_ZONE_ID: ["A", "B", "A"],
    }
    return pd.DataFrame.from_dict(data)


# SiteWatcher configuration


@pytest.fixture(scope="module")
def site_watcher():
    return SiteWatcher("https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile", 1)


@pytest.fixture(scope="module")
def dummy_http_response():
    class DummyHttpResponse:
        def __init__(self):
            self.headers = {
                "Date": "Sat, 27 Aug 2022 14:41:06 GMT",
                "Server": "Apache/2.4.7 (Ubuntu)",
                "X-Powered-By": "PHP/5.5.9-1ubuntu4.25",
                "Content-Disposition": 'attachment; filename="20030201_20030304.zip"',
                "Content-Length": "9145220",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "application/zip",
            }

    return DummyHttpResponse()


# ConnectionsParser configuration


@pytest.fixture(scope="module")
def connections_parser():
    return ConnectionsParser()


@pytest.fixture(scope="module")
def example_raw_stop_times_df():
    data = {
        COL_TRIP_ID: [
            "2_2182219^+",
            "2_2182219^+",
            "2_2182219^+",
            "2_2182219^+",
            "2_2182220^+",
            "2_2182220^+",
            "2_2182220^+",
            "2_2182221^+",
            "2_2182221^+",
        ],
        COL_ARRIVAL_TIME: [
            "06:00:00",
            "06:01:00",
            "06:03:00",
            "06:06:00",
            "12:30:00",
            "12:34:00",
            "12:38:00",
            "18:00:00",
            "18:00:00",
        ],
        COL_DEPARTURE_TIME: [
            "06:00:00",
            "06:01:00",
            "06:03:00",
            "06:06:00",
            "12:30:00",
            "12:34:00",
            "12:38:00",
            "18:00:00",
            "18:00:00",
        ],
        COL_STOP_ID: [1234, 5678, 9101, 1213, 2122, 2324, 2526, 9101, 1213],
        COL_STOP_SEQUENCE: [1, 2, 3, 4, 1, 2, 3, 1, 2],
        COL_STOP_HEADSIGN: [
            "OS. TEST",
            "OS. TEST",
            "OS. TEST",
            "OS. TEST",
            "TEST STREET",
            "TEST STREET",
            "TEST STREET",
            "OS. TEST",
            "OS. TEST",
        ],
        COL_PICKUP_TYPE: [1, 1, 3, 1, 3, 1, 1, 3, 1],
        COL_DROP_OFF_TYPE: [1, 1, 3, 1, 3, 1, 1, 3, 1],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture(scope="module")
def example_raw_trips_df():
    data = {
        COL_ROUTE_ID: ["T01", 100],
        COL_SERVICE_ID: [2, 4],
        COL_TRIP_ID: ["2_2182219^+", "2_2182220^+"],
        COL_TRIP_HEADSIGN: ["OS. TEST", "TEST STREET"],
        COL_DIRECTION_ID: [1, 0],
        COL_SHAPE_ID: [123456, 654321],
        COL_WHEELCHAIR_ACCESSIBLE: [0, 1],
        COL_BRIGADE: [1, 2],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture(scope="module")
def connections_batch():
    from_stop = RESULT_COL_FROM_STOP
    to_stop = RESULT_COL_TO_STOP
    lines = RESULT_COL_LINES
    return [
        {from_stop: 1234, to_stop: 5678, lines: ["T01"]},
        {from_stop: 5678, to_stop: 9101, lines: ["T01"]},
        {from_stop: 9101, to_stop: 1213, lines: ["T01"]},
        {from_stop: 2122, to_stop: 2324, lines: ["100"]},
        {from_stop: 2324, to_stop: 2526, lines: ["100"]},
    ]
