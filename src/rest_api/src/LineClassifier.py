from .exceptions import WrongLineFormatException


class LineClassifier:
    NIGHT_LINE_LENGTH = 3
    NIGHT_LINE_STARTING_CHAR = "2"

    @staticmethod
    def is_night_line(line: str) -> bool:
        """Checks if a line is a night line"""
        if len(line) < 1 or len(line) > 3:
            raise WrongLineFormatException(line)

        return (
            len(line) == LineClassifier.NIGHT_LINE_LENGTH
            and line[0] == LineClassifier.NIGHT_LINE_STARTING_CHAR
        )
