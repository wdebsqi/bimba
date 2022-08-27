import pandas as pd
import pytest

from ..src.FileParser import FileParser
from ..src.StopsParser import StopsParser
from ..src.SiteWatcher import SiteWatcher


@pytest.fixture(scope="module")
def parser():
    return StopsParser()


@pytest.fixture(scope="module")
def abstract_parser():
    return FileParser


@pytest.fixture(scope="module")
def example_raw_dataframe():
    data = {
        "stop_id": [1234, 5678, 9012],
        "stop_code": ["ABC1234", "DEF5678", "GHI9012"],
        "stop_name": ["ABC", "DEF", "GHI"],
        "stop_lat": [1.2, 2.3, 3.4],
        "stop_lon": [9.8, 8.7, 7.6],
        "zone_id": ["A", "B", "A"],
    }
    return pd.DataFrame.from_dict(data)


@pytest.fixture(scope="module")
def example_processed_dataframe():
    data = {
        "id": [1234, 5678, 9012],
        "name": ["ABC", "DEF", "GHI"],
        "lat": [1.2, 2.3, 3.4],
        "lon": [9.8, 8.7, 7.6],
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
