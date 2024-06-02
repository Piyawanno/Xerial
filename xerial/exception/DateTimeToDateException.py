from xerial.exception.ChangeTypeException import ChangeTypeException
from xerial.exception.ExceptionCode import ExceptionCode


class DateTimeToDateException(ChangeTypeException):
	def __init__(self, column: str):
		super(DateTimeToDateException, self).__init__()
		self.code = ExceptionCode.DATETIME_TO_DATE
		self.message = (f'Change type of column {column} '
						f'from DateTime to Date will result in time data loss')
