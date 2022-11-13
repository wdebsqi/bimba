class TestRoutePicker:
    def test_valid_routes(self, route_picker, valid_stop_names):
        for start_stop in valid_stop_names:
            for end_stop in valid_stop_names:
                if start_stop == end_stop:
                    continue
                route = route_picker.pick_best_route("name", start_stop, end_stop, True, False)
                assert isinstance(route, dict)
                assert route

    def test_invalid_routes(self, route_picker, invalid_stop_names):
        for start_stop in invalid_stop_names:
            for end_stop in invalid_stop_names:
                if start_stop == end_stop:
                    continue
                route = route_picker.pick_best_route("name", start_stop, end_stop, True, False)
                assert not route
