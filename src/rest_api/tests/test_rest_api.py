from flask import Flask

from ...db.models.neo4j import Stop


class TestRestApi:
    FIND_PATH_ROUTE = "/find_path"
    FIND_PATH_START_POINT = "start_point"
    FIND_PATH_END_POINT = "end_point"
    FIND_PATH_INCLUDE_DAYTIME = "include_daytime_lines"
    FIND_PATH_INCLUDE_NIGHTTIME = "include_nighttime_lines"
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
                            self.FIND_PATH_INCLUDE_DAYTIME: True,
                            self.FIND_PATH_INCLUDE_NIGHTTIME: False,
                        },
                    ).status_code
                    == 200
                )

    def test_find_path_endpoint_invalid_requests(
        self, client, invalid_stop_names, valid_stop_names
    ):
        assert client.get(self.FIND_PATH_ROUTE).status_code == 400

        for start_stop in invalid_stop_names:
            for end_stop in invalid_stop_names:
                assert (
                    client.get(
                        self.FIND_PATH_ROUTE,
                        data={
                            self.FIND_PATH_START_POINT: start_stop,
                            self.FIND_PATH_END_POINT: end_stop,
                            self.FIND_PATH_INCLUDE_DAYTIME: True,
                            self.FIND_PATH_INCLUDE_NIGHTTIME: False,
                        },
                    ).status_code
                    == 400
                )

        # also checking valid stops but only in case when the start and end stops are the same
        for start_stop in valid_stop_names:
            for end_stop in valid_stop_names:
                if start_stop == end_stop:
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
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [Stop.CODE, Stop.LON],
            },
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [Stop.NAME],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [Stop.NAME],
            },
            {
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [Stop.NAME, Stop.LAT, Stop.ZONE],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [Stop.ZONE, Stop.NAME],
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
                self.STOPS_ROUTE_REQUEST_BODY_KEY_PROPERTIES: [Stop.NAME],
                self.STOPS_ROUTE_REQUEST_BODY_KEY_DISTINCT: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED: True,
                self.STOPS_ROUTE_REQUEST_BODY_KEY_ORDERED_BY: [Stop.CODE],
            },
        ]

        for json in invalid_jsons:
            response = client.get(self.STOPS_ROUTE, json=json)
            assert response.status_code == 400
