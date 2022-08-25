class ForeignKey :
	def __init__(self, reference:str, parent) :
		self.reference = reference
		self.parent = parent
		splitted = reference.split(".")
		self.modelName = splitted[0]
		self.column = splitted[1]
		self.name = None
		self.model = None
		self.modelRecord = None
		self.columnMeta = None
	
	def fromDict(self, data:dict) :
		if self.modelRecord is None :
			self.modelRecord = self.model()
		return self.modelRecord.fromDict(data)