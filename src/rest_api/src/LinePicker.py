import pandas as pd


class LinePicker:
    """Class for picking the best line from the available lines."""

    def choose_most_occuring_line(
        self, lines_occurences_counted: pd.Series, lines_available: list
    ) -> str:
        """Returns the first line that is both available and has the highest number
        of occurences. Requires the parameter `lines_occurences_counted` to be a
        Pandas Series sorted in descending order."""
        for line in lines_occurences_counted.index:
            if line in lines_available:
                return line
