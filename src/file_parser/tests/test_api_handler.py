import pytest

from ..src.ZtmApiHandler import ZtmApiHandler


class TestApiHandler:
    @pytest.mark.parametrize("http_method", [ZtmApiHandler.HTTP_GET, ZtmApiHandler.HTTP_HEAD])
    def test_sending_successful_request(self, http_method, api_handler):
        assert api_handler.send_request(http_method).status_code == 200

    def test_checking_new_data_available(self, api_handler):
        assert api_handler.check_if_new_data_available("fake_filename.zip", "fake_hash") is True
