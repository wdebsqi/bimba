def test_log(logger):
    res = logger.log_message("test message", __file__, "test", False)
    assert res is True
