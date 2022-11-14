from flask import request


class TestRequestLogger:
    def test_log_request(self, app, request_logger):
        with app.test_request_context(
            path="/route_found",
            method="POST",
            data={
                "start_stop": "Rondo Rataje",
                "end_stop": "Rondo Starołęka",
                "include_day_lines": "on",
            },
        ):
            assert request_logger.log_request(request, with_commit=False)
