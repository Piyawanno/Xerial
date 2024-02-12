from xerial.Column import Column
from xerial.Vendor import Vendor

from fractions import Fraction
from typing import List

class FractionColumn (Column) :
	def __init__(self,
			isPrimary=False,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
			input=None) :
		Column.__init__(self,
			isPrimary=isPrimary,
			length=255,
			isNotNull=isNotNull,
			default=default,
			foreignKey=foreignKey,
			isIndex=isIndex,
			isRepresentative=isRepresentative,
			parentModel=parentModel,
			input=input
		)
		self.isConvertRaw = True
	
	def convertRaw(self, value) :
		return self.setValueToDB(value)
	
	def processValue(self, raw):
		if raw is None: return None
		return Fraction(raw)
	
	def toDict(self, attribute):
		if attribute is None :
			return None
		elif isinstance(attribute, str) :
			attribute = Fraction(attribute)

		return f"{attribute.numerator}/{attribute.denominator}"
	
	def fromDict(self, data) :
		raw = data.get(self.name, self.default)
		if raw is None :
			return None
		else :
			return Fraction(raw)
		
	def setValueToDB(self, attribute:Fraction) :
		if attribute is None: return "0"
		return f'{attribute.numerator}/{attribute.denominator}'
	
	def parseValue(self, value) :
		return Fraction(value)

	def getDBDataType(self) :
		if self.vendor == Vendor.MSSQL :
			return "NVARCHAR(255)"
		else :
			return "VARCHAR(255)"
	