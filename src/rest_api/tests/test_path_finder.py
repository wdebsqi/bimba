class TestPathFinder:
    def test_valid_paths(self, path_finder, valid_stop_names):
        for start_stop in valid_stop_names:
            for end_stop in valid_stop_names:
                if start_stop == end_stop:
                    continue
                path = path_finder.find_all_shortest_paths("name", start_stop, end_stop)
                assert isinstance(path, list)
                assert len(path) > 0

    def test_invalid_paths(self, path_finder, invalid_stop_names):
        for start_stop in invalid_stop_names:
            for end_stop in invalid_stop_names:
                if start_stop == end_stop:
                    continue
                path = path_finder.find_all_shortest_paths("name", start_stop, end_stop)
                assert isinstance(path, list)
                assert len(path) == 0
