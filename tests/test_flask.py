import pytest
from app import app


class TestFlask:
    @pytest.fixture(scope="class")
    def client(self):
        return app.test_client()

    def test_home(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert isinstance(res.json, dict)
        print(res.json.get("message"))
        assert res.json.get("message") == "Hello World!"

    def test_service(self, client):
        res = client.get("/service")
        assert res.status_code == 405
