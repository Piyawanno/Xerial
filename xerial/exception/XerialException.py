from xerial.exception.ExceptionCode import ExceptionCode


class XerialException(Exception):  # Change to something not Exception is possible
	def __init__(self, message: str = None):
		self.message = message
		self.code: ExceptionCode = ExceptionCode.XERIAL
		super().__init__(self.message)

	def __str__(self) -> str:
		return self.message
