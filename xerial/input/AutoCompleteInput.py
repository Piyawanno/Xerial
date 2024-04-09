from typing import Dict
from xerial.input.ReferenceSelectInput import ReferenceSelectInput
from xerial.InputAttachment import InputAttachment
class AutoCompleteInput (ReferenceSelectInput) :
	def __init__(
			self,
			label:str,
			url:str,
			prerequisite: str=None,
			prerequisiteParameterKey: str=None,
			tableURL:str=None,
			template:str="",
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
			typeName:str = 'AutoComplete',
		) :
		ReferenceSelectInput.__init__(
			self,
			label,
			url,
			tableURL,
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
			isStatusDisplay,
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
		self.template = template
		self.prerequisite = prerequisite
		self.prerequisiteParameterKey = prerequisiteParameterKey

	def toDict(self) -> dict:
		result = super().toDict()
		result['template'] = self.template
		result['prerequisite'] = self.prerequisite
		result['prerequisiteParameterKey'] = self.prerequisiteParameterKey
		return result