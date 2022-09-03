import pytest
from src.db.DBLogger import DBLogger


class TestDBLogger:
    @pytest.fixture(scope="class")
    def logger(self):
        return DBLogger()

    def test_log(self, logger):
        res = logger.log_message("test message", __file__, "test", False)
        assert res is True
