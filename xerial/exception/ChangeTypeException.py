from xerial.exception.ExceptionCode import ExceptionCode
from xerial.exception.ModificationException import ModificationException


class ChangeTypeException(ModificationException):
	def __init__(self):
		super(ChangeTypeException, self).__init__()
		self.code = ExceptionCode.CHANGE_TYPE
		self.message = 'Change Type Exception'
