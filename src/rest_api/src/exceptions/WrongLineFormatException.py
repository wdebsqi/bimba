class WrongLineFormatException(Exception):
    def __init__(self, line, message="Line name should be between 1 and 3 characters long"):
        self.line = line
        self.message = message
        super().__init__(self.message)
