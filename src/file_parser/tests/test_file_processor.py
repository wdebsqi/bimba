class TestFileProcessor:
    def test_parsing_filename_from_response_headers(self, file_processor, ztm_http_get_response):
        current_filename = file_processor.read_filename_from_response_header(ztm_http_get_response)
        assert current_filename[-4:] == ".zip"
