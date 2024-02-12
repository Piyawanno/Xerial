class XerialException(Exception):  # Change to something not Exception is possible
    def __init__(self, message):
        self.message = message
        self.code: int = 1
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

    def get_shifted_code(self):
        return self.code * 10
