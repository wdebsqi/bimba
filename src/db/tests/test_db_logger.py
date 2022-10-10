from ..DBLogger import DBLogger


def test_log(logger):
    res = logger.log_message("test message", __file__, logger.LOG_TYPE_TEST, False)
    assert res is True


def test_class_inheritance(logger):
    assert isinstance(logger, DBLogger)
