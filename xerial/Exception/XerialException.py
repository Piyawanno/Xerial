class XerialException(Exception):  # Change to something not Exception is possible
    def __init__(self, message: str = None):
        self.message = message
        self.code: int = 1
        super().__init__(self.message)

    def getMessage(self) -> str:
        return self.message

    def getShiftedCode(self) -> int:
        return self.code * 10
