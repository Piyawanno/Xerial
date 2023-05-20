from xerial.Column import Column
from datetime import datetime, date, timedelta

DATE_FORMAT = '%Y-%m-%d'

class DateColumn (Column) :
	@staticmethod
	def getToday() :
		return date.today().strftime(DATE_FORMAT)
	
	@staticmethod
	def getDayAfterToday(dayNumber:int) :
		def getDay() :
			day = date.today()+timedelta(days=dayNumber)
			return day.strftime(DATE_FORMAT)
		return getDay
	
	@staticmethod
	def getYearAfterToday(yearNumber:int) :
		def getDay() :
			today = date.today()
			day = date(year=today+yearNumber, month=today.month, day=today.day)
			return day.strftime(DATE_FORMAT)
		return getDay

	def fromDict(self, data):
		if self.name in data :
			raw = data.get(self.name, None)
			if raw is None : return None
			return datetime.strptime(raw, DATE_FORMAT).date()
		else :
			return datetime.now().date()

	def toDict(self, attribute):
		if attribute is None :
			return None
		elif isinstance(attribute, str) :
			attribute = datetime.strptime(attribute, DATE_FORMAT)
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