from xerial.Column import Column
from xerial.Vendor import Vendor
from typing import List

import time, math

DAY_SECONDS = 60*60*24

__INT_ULIMIT__ = 2**31
__INT_LLIMIT__ = -1*2**31
__BIG_INT_ULIMIT__ = 2**63
__BIG_INT_LLIMIT__ = -1*2**63

class IntegerColumn (Column) :
	isBigInt = False
	def __init__(self,
			isPrimary=False,
			length=32,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
			input=None,
			enum=None,
		) :
		
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
		self.enum = enum
		if self.length > 32 :
			self.isBigInt = True
	
	@staticmethod
	def getDateID() :
		return int(math.floor((time.time() - time.timezone) / DAY_SECONDS))
	
	def fromDict(self, data) :
		raw = data.get(self.name, self.default)
		if raw == "": raw = self.default
		if raw is None :
			return None
		else :
			result = self.default
			if type(raw) is str and '.' in raw:
				result = int(float(raw))
			else:
				result = int(raw)

			if self.isBigInt :
				if result > __BIG_INT_ULIMIT__ or result < __BIG_INT_LLIMIT__ :
					raise ValueError(f"Value {result} exceed limit.")
			else :
				if result > __INT_ULIMIT__ or result < __INT_LLIMIT__ :
					raise ValueError(f"Value {result}  exceed limit.")
			return result
	
	def toDict(self, attribute):
		from xerial.Record import Record
		if isinstance(attribute, Record) :
			return attribute.toDict()
		else :
			return attribute

	def setValueToDB(self, attribute) :
		return str(attribute)
	
	def parseValue(self, value) :
		if value == "": return self.default
		return int(value)

	def getDBDataType(self) :
		if self.vendor == Vendor.ORACLE :
			if self.length > 0 :
				length = 38 if self.length > 38 else self.length
				return "NUMBER(%d)"%(length)
			else :
				return "INTEGER"
		elif self.vendor == Vendor.MARIADB or self.vendor == Vendor.MYSQL :
			if self.length > 32 :
				return "BIGINT(%d)"%(self.length)
			else :
				return "INT(%d)"%(self.length)
		elif self.vendor == Vendor.SQLITE or self.vendor == Vendor.MSSQL :
			if self.length > 32 :
				return "BIGINT"
			else :
				return "INT"
		elif self.vendor == Vendor.POSTGRESQL:
			if self.isPrimary:
				return "BIGSERIAL"
			elif self.length > 32 :
				return "BIGINT"
			else :
				return "INT"
