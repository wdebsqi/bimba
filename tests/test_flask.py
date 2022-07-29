from app import flask_app


class TestFlask:
    client = flask_app.test_client()

    def test_home(self):
        res = self.client.get("/")
        assert res.status_code == 200
        assert isinstance(res.json, dict)
        print(res.json.get("message"))
        assert res.json.get("message") == "Hello World!"

    def test_service(self):
        res = self.client.get("/service")
        assert res.status_code == 405


if __name__ == "__main__":
    tester = TestFlask()
    tester.test_home()
    tester.test_service()
