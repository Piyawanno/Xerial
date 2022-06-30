from xerial.Column import Column
from xerial.Vendor import Vendor
from datetime import datetime

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class DateTimeColumn (Column) :
	def fromDict(self, data):
		if self.name in data :
			raw = data.get(self.name, None)
			if raw is None : return None
			return datetime.strptime(raw, DATETIME_FORMAT)
		else :
			return datetime.now()

	def toDict(self, attribute):
		if attribute is None :
			return None
		else :
			return attribute.strftime(DATETIME_FORMAT)

	def setValueToDB(self, attribute) :
		return "'%s'"%(attribute.strftime(DATETIME_FORMAT))

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE or self.vendor == Vendor.POSTGRESQL:
			return "TIMESTAMP"
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL or self.vendor == Vendor.SQLITE or self.vendor == Vendor.MSSQL:
			return "DATETIME"
