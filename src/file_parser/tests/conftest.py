import pandas as pd
import pytest

from ..src.FileParser import FileParser
from ..src.StopsParser import StopsParser


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
