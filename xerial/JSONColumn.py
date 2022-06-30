from xerial.Column import Column
from xerial.Vendor import Vendor

import json

class JSONColumn (Column) :
	def __init__(self, isNotNull=False, default=None) :
		Column.__init__(self,
			isPrimary=False,
			isNotNull=isNotNull,
			default=default,
		)

	def toDict(self, attribute):
		return attribute

	def fromDict(self, data) :
		return data.get(self.name, None)

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE or self.vendor == Vendor.SQLITE :
			return "CLOB"
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL :
			return "LONGTEXT COLLATE utf8mb4_unicode_ci"
		elif self.vendor == Vendor.POSTGRESQL :
			return "JSON"
		elif self.vendor == Vendor.MSSQL :
			return "TEXT"
		
	def setValueToDB(self, attribute) :
		return "'%s'"%(json.dumps(attribute))