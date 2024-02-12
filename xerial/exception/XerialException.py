class XerialException(Exception):  # Change to something not Exception is possible
    def __init__(self, message: str = None):
        self.message = message
        self.code: int = 1
        super().__init__(self.message)

    def get_message(self) -> str:
        return self.message

    def get_shifted_code(self) -> int:
        return self.code * 10
