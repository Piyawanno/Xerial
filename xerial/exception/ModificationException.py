from xerial.exception.ExceptionCode import ExceptionCode
from xerial.exception.XerialException import XerialException


class ModificationException(XerialException):
	def __init__(self):
		super(ModificationException, self).__init__()
		# manually assign per category, modification is 1
		self.code = ExceptionCode.MODIFICATION
		self.message = 'ModificationAction Exception'
