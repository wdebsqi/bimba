from flask import Flask


class TestRestApi:
    FIND_PATH_ROUTE = "/find_path"
    FIND_PATH_START_POINT = "start_point"
    FIND_PATH_END_POINT = "end_point"

    def test_app_instance(self, app):
        assert isinstance(app, Flask)

    def test_find_path_endpoint_valid_requests(self, client, valid_stop_names):
        for start_stop in valid_stop_names:
            for end_stop in valid_stop_names:
                if start_stop == end_stop:
                    continue

                assert (
                    client.get(
                        self.FIND_PATH_ROUTE,
                        data={
                            self.FIND_PATH_START_POINT: start_stop,
                            self.FIND_PATH_END_POINT: end_stop,
                        },
                    ).status_code
                    == 200
                )

    def test_find_path_endpoint_invalid_requests(self, client, invalid_stop_names):
        assert client.get(self.FIND_PATH_ROUTE).status_code == 400

        for start_stop in invalid_stop_names:
            for end_stop in invalid_stop_names:
                if start_stop == end_stop:
                    continue

                assert (
                    client.get(
                        self.FIND_PATH_ROUTE,
                        data={
                            self.FIND_PATH_START_POINT: start_stop,
                            self.FIND_PATH_END_POINT: end_stop,
                        },
                    ).status_code
                    == 400
                )
