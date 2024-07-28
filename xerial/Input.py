from typing import Dict, List
from packaging.version import Version
from xerial.InputAttachment import InputAttachment
from xerial.input.SideIcon import SideIcon
from xerial.Filter import Filter

class Input :
	def __init__(
			self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isAdvanceForm:bool=False,
			isTableForm:bool=False,
			isView:bool=False,
			isSearchTable:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			help:str=None,
			documentPath:str=None,
			config: Dict=None,
			columnType:str='',
			columnName:str='',
			sideIcon:List[SideIcon]=[],
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine: int=None,
			filter: Filter=None,
			placeHolder:str=None,
			typeName:str=None,
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
		self.isView = isView 
		self.isTableForm = isTableForm
		self.isSearchTable = isSearchTable
		self.isAdvanceForm = isAdvanceForm
		self.attachedGroup = attachedGroup
		self.attachedGroupID = None
		self.help = help
		self.documentPath = documentPath
		self.config = config
		self.parsedOrder = Version(order) if order is not None else None
		self.typeName = typeName
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
		self.isCopyable = isCopyable
		self.inputPerLine = inputPerLine
		self.filter = filter
		self.childrenModelName = None
		self.isTag = False
		self.placeHolder = placeHolder
	
	def setOrderAttribute(self, column):
		pass
	
	def toDict(self) -> dict :
		groupValue = self.group if self.group is None or isinstance(self.group, int) else self.group.value
		return {
			'columnName' : self.columnName,
			'columnType' : self.columnType,
			'label' : self.label,
			'order' : self.order,
			'group' : groupValue,
			'isTable' : self.isTable,
			'isMobile' : self.isMobile,
			'isSearch' : self.isSearch,
			'isRequired' : self.isRequired,
			'isEditable' : self.isEditable,
			'isNumber' : self.isNumber,
			'isFile' : self.isFile,
			'isForm' : self.isForm,
			'isView' : self.isView,
			'isTableForm' : self.isTableForm,
			'isSearchTable': self.isSearchTable,
			'isAdvanceForm' : self.isAdvanceForm,
			'attachedGroupID': self.attachedGroupID,
			'help' : self.help,
			'documentPath' : self.documentPath,
			'typeName' : self.typeName,
			'foreignModelName' : self.foreignModelName,
			'foreignColumn' : self.foreignColumn,
			'isLink' : self.isLink,
			'linkColumn' : self.linkColumn,
			'sideIcon': [] if self.sideIcon is None else [i.toDict() for i in self.sideIcon],
			'isCopyable': self.isCopyable,
			'inputPerLine': self.inputPerLine,
			'filter': None if self.filter is None else self.filter.toDict(),
			'childrenModelName': self.childrenModelName,
			'isTag': self.isTag,
			'placeHolder': self.placeHolder,
		}
	