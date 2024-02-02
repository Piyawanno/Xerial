from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment

class PrerequisiteReferenceSelectInput (Input):
	def __init__(self,
			label:str,
			url:str,
			prerequisite: str,
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
			isAdvanceFrom:bool=False,
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
			isAdvanceFrom,
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
		)
		self.url = url
		self.tableURL = tableURL
		self.prerequisite = prerequisite
		self.isLink = isLink
		self.typeName = 'PrerequisiteReferenceSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		result['tableURL'] = self.tableURL
		result['prerequisite'] = self.prerequisite
		return result