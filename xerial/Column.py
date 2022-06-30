from dataclasses import field

class Column :
	def __init__(self, isPrimary=False, length=0, isNotNull=False, default=None, foreignKey=None, isIndex=False, input=None) :
		self.length = length
		if foreignKey is not None :
			self.foreignKey = foreignKey.split(".")
		else :
			self.foreignKey = None
		self.isPrimary = isPrimary
		self.name = ''
		self.isNotNull = isNotNull
		self.default = default
		self.isIndex = isIndex
		self.input = input
	
	def getReference(self, attribute) :
		if self.foreignKey is None :
			raise ValueError("Column %s has no foreignKey."%(self.name))
		else :
			return getattr(attribute, self.foreignKey[1])
	
	def getParameterFormat(self) :
		return f"%({self.name})s"
	
	def processValue(self, raw) :
		return raw
	
	def setValueToDB(self, attribute) :
		return attribute
	
	def toDict(self, attribute):
		return attribute
	
	def fromDict(self, data) :
		raise NotImplementedError
	
	def getDBDataType(self) :
		raise NotImplementedError

	def parseSelect(self) :
		return self.name