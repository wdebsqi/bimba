from flask import Flask

from ..src.StopsGetter import STOP_CODE, STOP_LAT, STOP_LON, STOP_NAME, STOP_ZONE


class TestRestApi:
    FIND_PATH_ROUTE = "/find_path"
    FIND_PATH_START_POINT = "start_point"
    FIND_PATH_END_POINT = "end_point"
    STOPS_ROUTE = "/stops"
    STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES = "properties"
    STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT = "distinct"
    STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED = "ordered"
    STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY = "ordered_by"

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

    def test_stops_endpoint_valid_requests(self, client):
        valid_jsons = [
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [STOP_CODE, STOP_LON],
            },
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [STOP_NAME],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [STOP_NAME],
            },
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [STOP_NAME, STOP_LAT, STOP_ZONE],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [STOP_ZONE, STOP_NAME],
            },
        ]

        for json in valid_jsons:
            response = client.get(self.STOPS_ROUTE, json=json)
            assert response.status_code == 200
            assert isinstance(response.json, list)

    def test_stops_endpoint_invalid_requests(self, client):
        invalid_jsons = [
            None,
            {self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True},
            {self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: []},
            {self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: ["not", "real", "properties"]},
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [STOP_NAME],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [STOP_CODE],
            },
        ]

        for json in invalid_jsons:
            response = client.get(self.STOPS_ROUTE, json=json)
            assert response.status_code == 400
