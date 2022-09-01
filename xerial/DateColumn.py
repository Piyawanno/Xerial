from xerial.Column import Column
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

class DateColumn (Column) :
	def fromDict(self, data):
		if self.name in data :
			raw = data.get(self.name, None)
			if raw is None : return None
			return datetime.strptime(raw, DATE_FORMAT).date()
		else :
			return datetime.now().date()

	def toDict(self, attribute):
		if type(attribute) == str: attribute = datetime.strptime(attribute, DATE_FORMAT)
		return attribute.strftime(DATE_FORMAT)
		
	def setValueToDB(self, attribute) :
		return "'%s'"%(attribute.strftime(DATE_FORMAT))
	
	def parseValue(self, value) :
		return datetime.strptime(value, DATE_FORMAT)

	def getDBDataType(self) :
		return "DATE"

	@staticmethod
	def getStartDate(data) :
		if isinstance(data, datetime) :
			return datetime(year=data.year, month=data.month, day=data.day, hour=0, minute=0, second=0)
		else :
			raise TypeError