import pytest

from ..DBLogger import DBLogger


@pytest.fixture(scope="module")
def logger():
    return DBLogger()
