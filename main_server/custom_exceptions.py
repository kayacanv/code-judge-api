
class InvalidInputError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MissingParameterError(InvalidInputError):
    def __init__(self, parameter):
        self.parameter = parameter
        self.message = f"Missing required parameter: {self.parameter}"
        super().__init__(self.message)
