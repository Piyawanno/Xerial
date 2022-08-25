from packaging.version import Version

class Input :
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			documentPath:str=None,
		):
		self.label = label
		self.order = order
		self.group = group
		self.isTable = isTable
		self.isSearch = isSearch
		self.isRequired = isRequired
		self.isEditable = isEditable
		self.help = help
		self.documentPath = documentPath
		self.parsedOrder = Version(order) if order is not None else None
		self.typeName = ''
		self.columnName = ''
		self.columnType = ''
	
	def toDict(self) -> dict :
		return {
			'columnName' : self.columnName,
			'columnType' : self.columnType,
			'label' : self.label,
			'order' : self.order,
			'group' : self.group,
			'isTable' : self.isTable,
			'isSearch' : self.isSearch,
			'isRequired' : self.isRequired,
			'isEditable' : self.isEditable,
			'help' : self.help,
			'documentPath' : self.documentPath,
			'typeName' : self.typeName
		}
	