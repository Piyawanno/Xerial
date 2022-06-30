from packaging import version

class Input :
	def __init__(self, label:str, order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False):
		self.label = label
		self.order = order
		self.isTable = isTable
		self.isSearch = isSearch
		self.isRequired = isRequired
		self.parsedOrder = version.parse(order) if order is not None else None
		self.typeName = ''
		self.columnName = ''
		self.columnType = ''
	
	def toDict(self) -> dict :
		return {
			'columnName' : self.columnName,
			'columnType' : self.columnType,
			'label' : self.label,
			'order' : self.order,
			'isTable' : self.isTable,
			'isSearch' : self.isSearch,
			'isRequired' : self.isRequired,
			'typeName' : self.typeName
		}
	