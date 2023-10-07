# NOTE
# This structure is additional structure to ModelClass.
# In regular operation, the structure is not required.
# For some special operations, in which data will not mapped to
# Records but directly used, this structure can be helpful.
# For example, writing .xlsx file.

from xerial.ForeignKey import ForeignKey

class PrimitiveStructure :
	def __init__(self, modelClass) :
		self.modelClass = modelClass
		self.processColumn()
		self.processForeign()
	
	def processColumn(self) :
		self.columnNameIndex = {}
		self.enumLabel = []
		for i, (columnName, column) in enumerate(self.modelClass.meta) :
			self.columnNameIndex[columnName] = i
			if hasattr(column, 'enum') and column.enum is not None :
				if hasattr(column.enum, 'label') :
					self.enumLabel.append((i, column.enum.label))
				else :
					self.enumLabel.append((i, {i.value:str(i) for i in column.enum}))
	
	def processForeign(self) :
		self.foreignIndex = {}
		self.foreignIndexMapper = {}
		foreignKey:ForeignKey
		for foreignKey in self.modelClass.foreignKey :
			index = self.columnNameIndex[foreignKey.name]
			self.foreignIndex[foreignKey.name] = index
			self.foreignIndexMapper[index] = foreignKey
			foreignKey.processEnumLabel()