from xerial.Column import Column
from xerial.Vendor import Vendor
from typing import List
class StringColumn (Column) :
	isCLOB = False
	def __init__(self,
			isPrimary=False,
			length=255,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
			isFixedLength=False,
			input=None) :
			
		Column.__init__(self,
			isPrimary=isPrimary,
			length=length,
			isNotNull=isNotNull,
			default=default,
			foreignKey=foreignKey,
			isIndex=isIndex,
			isRepresentative=isRepresentative,
			parentModel=parentModel,
			input=input
		)
		self.isFixedLength = isFixedLength
		if self.length < 0 :
			self.isCLOB = True

	def toDict(self, attribute):
		return attribute.read() if self.isCLOB and hasattr(attribute, 'read') else attribute

	def fromDict(self, data) :
		value = data.get(self.name, None)
		if value is None: return value
		if not type(value) is str: value = str(value)
		return value

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			if self.isCLOB or self.length < 0 or self.length > 2000:
				return "CLOB"
			elif self.isFixedLength :
				return "CHAR(%d)"%(self.length)
			else :
				return "VARCHAR(%d)"%(self.length)
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL:
			if 0 < self.length < 256 :
				if self.isFixedLength :
					return "CHAR(%d) COLLATE utf8mb4_unicode_ci"%(self.length)
				else :
					return "VARCHAR(%d) COLLATE utf8mb4_unicode_ci"%(self.length)
			else :
				return "LONGTEXT COLLATE utf8mb4_unicode_ci"
		elif self.vendor == Vendor.POSTGRESQL or self.vendor == Vendor.SQLITE :
			if self.isCLOB :
				return "TEXT"
			elif 0 < self.length < 256 :
				if self.isFixedLength :
					return "CHAR(%d)"%(self.length)
				else :
					return "VARCHAR(%d)"%(self.length)
			else :
				return "TEXT"
		elif self.vendor == Vendor.MSSQL :
			if 0 < self.length < 256 :
				if self.isFixedLength :
					return "NCHAR(%d)"%(self.length)
				else :
					return "NVARCHAR(%d)"%(self.length)
			else :
				return "TEXT "

	
	def setValueToDB(self, attribute) :
		return "'%s'"%(attribute)
	
	def parseValue(self, value) :
		return value