from typing import Dict
from packaging.version import Version

class Input :
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			help:str=None,
			documentPath:str=None,
			config: Dict=None,
			columnType:str='',
			columnName:str='',			
		):
		self.label = label
		self.order = order
		self.group = group
		self.isTable = isTable
		self.isMobile = isMobile
		self.isSearch = isSearch
		self.isRequired = isRequired
		self.isEditable = isEditable
		self.isForm = isForm
		self.help = help
		self.documentPath = documentPath
		self.config = config
		self.parsedOrder = Version(order) if order is not None else None
		self.typeName = ''
		self.columnName = columnName
		self.columnType = columnType
		self.isNumber = False
		self.isFile = False
	
	def toDict(self) -> dict :
		return {
			'columnName' : self.columnName,
			'columnType' : self.columnType,
			'label' : self.label,
			'order' : self.order,
			'group' : self.group,
			'isTable' : self.isTable,
			'isMobile' : self.isMobile,
			'isSearch' : self.isSearch,
			'isRequired' : self.isRequired,
			'isEditable' : self.isEditable,
			'isNumber' : self.isNumber,
			'isFile' : self.isFile,
			'isForm' : self.isForm,
			'help' : self.help,
			'documentPath' : self.documentPath,
			'typeName' : self.typeName,
		}
	