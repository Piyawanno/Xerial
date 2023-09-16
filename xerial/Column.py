from xerial.ForeignKey import ForeignKey
from xerial.Vendor import Vendor

from typing import List
class Column :
	compatible = set()
	def __init__(self,
			isPrimary=False,
			length=0,
			isNotNull=False,
			default=None,
			foreignKey=None,
			isIndex=False,
			isRepresentative=False,
			parentModel:List[type]=[],
			input=None
		) :
		
		from xerial.Input import Input
		self.length = length
		if foreignKey is not None :
			self.foreignKey = ForeignKey(foreignKey, self)
		else :
			self.foreignKey = None
		self.isPrimary = isPrimary
		self.name = ''
		self.isNotNull = isNotNull
		self.default = default
		self.isIndex = isIndex
		self.isRepresentative = isRepresentative
		self.parentModel = parentModel
		self.input:Input = input
		if input is not None : input.attribute = self
		self.isConvertRaw = False
	
	def convertRaw(self, value) :
		return value
	
	def getReference(self, attribute) :
		if self.foreignKey is None :
			raise ValueError("Column %s has no foreignKey."%(self.name))
		else :
			return getattr(attribute, self.foreignKey.column)
	
	def getParameterFormat(self) :
		return f"%({self.name})s"
	
	def processValue(self, raw) :
		if self.vendor == Vendor.POSTGRESQL:
			from asyncpg.pgproto.pgproto import UUID
			if type(raw) == UUID:
				raw = str(raw)
		return raw
	
	def setValueToDB(self, attribute) :
		return attribute
	
	def parseValue(self, value) :
		return value
	
	def toDict(self, attribute):
		return attribute
	
	def fromDict(self, data) :
		raise NotImplementedError
	
	def checkReferenceFromDict(self, data) :
		raw = data.get(self.name, None)
		if isinstance(raw, dict) and self.foreignKey is not None :
			return self.foreignKey.model().fromDict(raw)
		else :
			return None
	
	def getDBDataType(self) :
		raise NotImplementedError

	def parseSelect(self) :
		return self.name