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

		self.enumLabel = None
		self.representativeColumn = -1
	
	def fromDict(self, data:dict) :
		self.modelRecord = self.model()
		return self.modelRecord.fromDict(data)

	def processEnumLabel(self) :
		if self.enumLabel is not None : return
		self.enumLabel = []
		for i, (columnName, column) in enumerate(self.model.meta) :
			if column.isRepresentative : self.representativeColumn = i
			if hasattr(column, 'enum') and column.enum is not None :
				if hasattr(column.enum, 'label') :
					self.enumLabel.append((i, column.enum.label))
				else :
					self.enumLabel.append((i, {i.value:str(i) for i in column.enum}))