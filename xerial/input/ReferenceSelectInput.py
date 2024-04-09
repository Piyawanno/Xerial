from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment

class ReferenceSelectInput (Input):
	def __init__(
			self,
			label:str,
			url:str,
			tableURL:str=None,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			isTableForm:bool=False,
			isSearchTable:bool=False,
			isAdvanceForm:bool=False,
			isStatusDisplay:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
			sideIcon:str=None,
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine:int=None,
			typeName:str = 'ReferenceSelect',
		) :
		Input.__init__(
			self,
			label,
			order,
			group,
			isTable,
			isMobile,
			isSearch,
			isRequired,
			isEditable,
			isForm,
			isTableForm,
			isSearchTable,
			isAdvanceForm,
			attachedGroup,
			isLink,
			linkColumn,
			help,
			documentPath,
			config,
			columnType,
			columnName,
			sideIcon,
			isEnabled,
			isSpreadSheet,
			isCopyable,
			inputPerLine,
			typeName,
		)
		self.url = url
		self.tableURL = tableURL
		self.isStatusDisplay = isStatusDisplay
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		result['tableURL'] = self.tableURL
		result['isLink'] = self.isLink
		result['isStatusDisplay'] = self.isStatusDisplay
		return result