import pandas as pd


class TestLinePicker:
    LINES_THAT_SHOULD_BE_AVAILABLE = ["T12", "2", "3"]
    LINES_THAT_SHOULD_NOT_BE_AVAILABLE = ["6", "12", "420"]
    LINES_OCCURENCES = pd.Series(
        index=["T12", "4", "822", "3", "17", "3", "222"], data=[1, 2, 3, 4, 5, 6, 7]
    )

    def test_available_lines_picking(self, line_picker):
        line_picked = line_picker.choose_most_occuring_line(
            self.LINES_OCCURENCES, self.LINES_THAT_SHOULD_BE_AVAILABLE
        )
        assert line_picked
        assert line_picked in self.LINES_THAT_SHOULD_BE_AVAILABLE

    def test_not_available_lines_picking(self, line_picker):
        line_picked = line_picker.choose_most_occuring_line(
            self.LINES_OCCURENCES, self.LINES_THAT_SHOULD_NOT_BE_AVAILABLE
        )
        assert not line_picked
