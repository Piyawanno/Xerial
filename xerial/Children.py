class Children :
	def __init__(self, reference:str) :
		self.reference = reference
		splitted = reference.split(".")
		self.modelName = splitted[0]
		self.column = splitted[1]
		self.parentColumn = None
		self.name = None
		self.model = None

	def fromDict(self, data:list) :
		return [self.model().fromDict(i) for i in data]