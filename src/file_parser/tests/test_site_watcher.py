from requests import Response


class TestSiteWatcher:
    def test_filenames_parsing(self, site_watcher):
        current_filename = site_watcher.get_current_filename()
        assert current_filename is None

        response = site_watcher.query_site(site_watcher.HTTP_HEAD)
        assert isinstance(response, Response)
        site_watcher.check_if_new_data_available(response)
        current_filename = site_watcher.get_current_filename()
        assert current_filename[-4:] == ".zip"

    def test_parsing_filename_from_response_headers(self, site_watcher, dummy_http_response):
        header = site_watcher._extract_response_header(
            dummy_http_response, site_watcher.HEADER_FILENAME_KEY
        )
        assert header == 'attachment; filename="20030201_20030304.zip"'

        filename = site_watcher._read_filename_from_response_header(header)
        assert filename == "20030201_20030304.zip"

    def test_checking_new_data_available(self, site_watcher):
        response = site_watcher.query_site(site_watcher.HTTP_HEAD)
        assert not site_watcher.check_if_new_data_available(response)

        site_watcher._last_filename = "20000000_20010101.zip"
        assert site_watcher.check_if_new_data_available(response)
        assert not site_watcher.check_if_new_data_available(response)
