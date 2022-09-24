import pandas as pd
import pytest

from ..src.ConnectionsParser import ConnectionsParser
from ..src.FileParser import FileParser
from ..src.SiteWatcher import SiteWatcher
from ..src.StopsParser import StopsParser


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
        "stop_id": [1234, 5678, 9012],
        "stop_code": ["ABC1234", "DEF5678", "GHI9012"],
        "stop_name": ["ABC", "DEF", "GHI"],
        "stop_lat": [1.2, 2.3, 3.4],
        "stop_lon": [9.8, 8.7, 7.6],
        "zone_id": ["A", "B", "A"],
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
        "trip_id": [
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
        "arrival_time": [
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
        "departure_time": [
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
        "stop_id": [1234, 5678, 9101, 1213, 2122, 2324, 2526, 9101, 1213],
        "stop_sequence": [1, 2, 3, 4, 1, 2, 3, 1, 2],
        "stop_headsign": [
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
        "pickup_type": [1, 1, 3, 1, 3, 1, 1, 3, 1],
        "drop_off_type": [1, 1, 3, 1, 3, 1, 1, 3, 1],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture(scope="module")
def example_raw_trips_df():
    data = {
        "route_id": ["T01", "100"],
        "service_id": [2, 4],
        "trip_id": ["2_2182219^+", "2_2182220^+"],
        "trip_headsign": ["OS. TEST", "TEST STREET"],
        "direction_id": [1, 0],
        "shape_id": [123456, 654321],
        "wheelchair_accessible": [0, 1],
        "brigade": [1, 2],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture(scope="module")
def connections_batch():
    from_stop = "from_stop"
    to_stop = "to_stop"
    line = "line"
    return [
        {from_stop: 1234, to_stop: 5678, line: "T01"},
        {from_stop: 5678, to_stop: 9101, line: "T01"},
        {from_stop: 9101, to_stop: 1213, line: "T01"},
        {from_stop: 2122, to_stop: 2324, line: "100"},
        {from_stop: 2324, to_stop: 2526, line: "100"},
    ]
