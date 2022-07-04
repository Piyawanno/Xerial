class ForeignKey :
	def __init__(self, reference:str) :
		self.reference = reference
		splitted = reference.split(".")
		self.modelName = splitted[0]
		self.column = splitted[1]
		self.name = None
		self.model = None
	
	def fromDict(self, data:dict) :
		return self.model().fromDict(data)