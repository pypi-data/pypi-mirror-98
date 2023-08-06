class InvalidCredentials(Exception):
    """Exception raised for invalid credentials.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
