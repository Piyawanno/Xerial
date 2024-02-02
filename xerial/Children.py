class Children :
	def __init__(self, reference:str, isTableForm:bool=False, title:str='') :
		self.reference = reference
		splitted = reference.split(".")
		self.modelName = splitted[0]
		self.column = splitted[1]
		self.isTableForm = isTableForm
		self.parentColumn = None
		self.name = None
		self.model = None
		self.title = title

	def fromDict(self, data:list) :
		return [self.model().fromDict(i) for i in data]
	
	def toMetaDict(self) :
		return {
			'reference': self.reference,
			'modelName': self.modelName,
			'column': self.column,
			'isTableForm': self.isTableForm,
			'parentColumn': self.parentColumn,
			'name': self.name,
			'title': self.title
		}