from flask import Flask


class TestFrontend:
    ROUTE_HOME = "/"
    ROUTES = [ROUTE_HOME]
    ROUTE_ERROR_400 = "/error_400"
    ROUTES_ERROR = [ROUTE_ERROR_400]

    def test_class_inheritance(self, app):
        assert isinstance(app, Flask)

    def test_routes_responses(self, client):
        for route in self.ROUTES:
            response = client.get(route)
            assert response.status_code == 200

    def test_error_responses(self, client):
        for route in self.ROUTES_ERROR:
            response = client.get(route)
            assert response.status_code == 400
