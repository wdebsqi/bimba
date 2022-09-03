from datetime import datetime

import pytest
from src.db.DBLogger import DBLogger

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class TestDBLogger:
    @pytest.fixture(scope="class")
    def logger(self):
        return DBLogger()

    def test_log(self, logger):
        now = datetime.now().strftime(TIMESTAMP_FORMAT)
        res = logger.log_message(now, "test message", __file__, "test", False)
        assert res is True
