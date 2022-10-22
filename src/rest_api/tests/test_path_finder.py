from random import choice


class TestPathFinder:
    def _randomize_string_case(self, input_string: str) -> str:
        """Randomizes the case of each character in the input string.
        Doesn't randomize Polish special characters as they are case-sensitive."""
        chars_not_to_change = ["ą", "ć", "ę", "ł", "ń", "ó", "ś", "ź", "ż"]
        return "".join(
            choice((str.lower, str.upper))(char) if char not in chars_not_to_change else char
            for char in input_string
        )

    def test_valid_paths(self, path_finder, valid_stop_names):
        for start_stop in valid_stop_names:
            for end_stop in valid_stop_names:
                if start_stop == end_stop:
                    continue

                start_stop_random_case = self._randomize_string_case(start_stop)
                end_stop_random_case = self._randomize_string_case(end_stop)
                path = path_finder.find_all_shortest_paths(
                    "name", start_stop_random_case, end_stop_random_case
                )
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
