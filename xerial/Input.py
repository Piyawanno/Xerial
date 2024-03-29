from typing import Dict
from packaging.version import Version
from xerial.InputAttachment import InputAttachment

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
			isTableForm:bool=False,
			isAdvanceFrom:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			help:str=None,
			documentPath:str=None,
			config: Dict=None,
			columnType:str='',
			columnName:str='',
			sideIcon:str=None,
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
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
		self.isTableForm = isTableForm
		self.isAdvanceForm = isAdvanceFrom
		self.attachedGroup = attachedGroup
		self.attachedGroupID = None
		self.help = help
		self.documentPath = documentPath
		self.config = config
		self.parsedOrder = Version(order) if order is not None else None
		self.typeName = ''
		self.columnName = columnName
		self.columnType = columnType
		self.isLink = isLink
		self.linkColumn = linkColumn
		self.sideIcon = sideIcon
		self.foreignModelName = None
		self.foreignColumn = None
		self.isNumber = False
		self.isFile = False
		self.attribute = None
		self.isEnabled = isEnabled
		self.isSpreadSheet = isSpreadSheet
	
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
			'isTableForm' : self.isTableForm,
			'isAdvanceForm' : self.isAdvanceForm,
			'attachedGroupID': self.attachedGroupID,
			'help' : self.help,
			'documentPath' : self.documentPath,
			'typeName' : self.typeName,
			'foreignModelName' : self.foreignModelName,
			'foreignColumn' : self.foreignColumn,
			'isLink' : self.isLink,
			'linkColumn' : self.linkColumn,
			'sideIcon': self.sideIcon,
		}
	