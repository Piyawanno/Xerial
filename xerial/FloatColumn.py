from xerial.Column import Column
from xerial.Vendor import Vendor
from typing import List
class FloatColumn (Column) :
	def __init__(self,
			isPrimary=False,
			length=32,
			precision=8,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
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
		self.precision = precision
	
	def fromDict(self, data) :
		raw = data.get(self.name, self.default)
		if raw == "": raw = self.default
		if raw is None :
			return None
		else :
			return float(raw)
		
	def setValueToDB(self, attribute) :
		return str(attribute)
	
	def parseValue(self, value) :
		return float(value)

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			return "NUMBER(%d, %d)"%(self.length, self.precision)
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL :
			return "DOUBLE"
		elif self.vendor == Vendor.POSTGRESQL or self.vendor == Vendor.SQLITE:
			return "DOUBLE PRECISION"
		elif self.vendor == Vendor.MSSQL :
			return "FLOAT(53)"