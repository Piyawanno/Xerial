from xerial.Column import Column
from xerial.Vendor import Vendor
from xerial.CurrencyData import CurrencyData
from typing import List

import json

class CurrencyColumn (Column) :
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
		if value is None: return None
		return json.dumps(value.toDict())
	
	def processValue(self, raw):
		if raw is None: return None
		parsed = json.loads(raw)
		return CurrencyData(0).fromDict(parsed)
	
	def toDict(self, attribute):
		return attribute.toDict()
	
	def fromDict(self, raw) :
		if raw is None :
			return None
		else :
			if raw.get('originString', None) is None:
				raw = raw.get(self.name, self.default)
			return CurrencyData(0).fromDict(raw)
		
	def setValueToDB(self, attribute:CurrencyData) :
		if attribute is None: return None
		return "'%s'"%(json.dumps(attribute.toDict()))
	
	def parseValue(self, value) :
		parsed = json.loads(value)
		return CurrencyData(0).fromDict(parsed)

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE or self.vendor == Vendor.SQLITE :
			return "CLOB"
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL :
			return "LONGTEXT COLLATE utf8mb4_unicode_ci"
		elif self.vendor == Vendor.POSTGRESQL :
			return "JSON"
		elif self.vendor == Vendor.MSSQL :
			return "TEXT"
	