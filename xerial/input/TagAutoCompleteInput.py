from typing import Dict
from xerial.input.AutoCompleteInput import AutoCompleteInput
from xerial.InputAttachment import InputAttachment
from xerial.Filter import Filter
class TagAutoCompleteInput (AutoCompleteInput) :
	def __init__(
			self,
			label:str,
			url:str,
			prerequisite: str=None,
			prerequisiteParameterKey: str=None,
			tableURL:str=None,
			childrenURL:str=None,
			childrenColumn:str=None,
			template:str="",
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
			filter: Filter=None,
			placeHolder:str=None,
			typeName:str = 'TagAutoComplete',
		) :
		AutoCompleteInput.__init__(
			self,
			label,
			url,
			prerequisite,
			prerequisiteParameterKey,
			tableURL,
			template,
			order,
			group,
			isTable,
			isMobile,
			isSearch,
			isRequired,
			isEditable,
			isForm,
			isAdvanceForm,
			isTableForm,
			isView,
			isSearchTable,
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
			filter,
			placeHolder,
			typeName,
		)
		self.childrenURL = childrenURL
		self.childrenColumn = childrenColumn
		self.isTag = True

	def toDict(self) -> dict :
		data = AutoCompleteInput.toDict(self)
		data['childrenURL'] = self.childrenURL
		data['childrenColumn'] = self.childrenColumn
		return data