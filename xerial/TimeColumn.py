from xerial.Column import Column
from xerial.Vendor import Vendor

from datetime import timedelta, datetime, time

TIME_FORMAT = '%H:%M:%S'

class TimeColumn (Column) :
	def fromDict(self, data):
		if self.name in data :
			raw = data[self.name]
			if raw is None : return None
			if len(raw) == 5 : raw += ":00"
			return datetime.strptime(raw, TIME_FORMAT).time()
		else :
			return datetime.now().time()

	def toDict(self, attribute):
		if isinstance(attribute, timedelta) :
			return self.parseTime(attribute)
		elif isinstance(attribute, time) :
			return attribute.strftime(TIME_FORMAT)

	def setValueToDB(self, attribute) :
		if isinstance(attribute, timedelta) :
			return "'%s'"%(self.parseTime(attribute))
		else :
			return "'%s'"%(attribute.strftime(TIME_FORMAT))
	
	def parseValue(self, value) :
		return datetime.strptime(value, TIME_FORMAT)
	
	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			return "INTERVAL DAY TO SECOND"
		else :
			return "TIME"
	
	@staticmethod
	def toSeconds(data) :
		if isinstance(data, timedelta) :
			return data.seconds
		elif isinstance(data, time) or isinstance(data, datetime):
			return 3600*data.hour + 60*data.minute + data.second
		else :
			raise TypeError

	@staticmethod
	def parseTime(delta):
		hours, remainder = divmod(delta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		return "%02d:%02d:%02d" % (hours, minutes, seconds)