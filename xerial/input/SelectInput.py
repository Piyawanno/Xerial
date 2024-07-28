from xerial.Input import Input
from xerial.input.TableDisplayType import TableDisplayType
from xerial.InputAttachment import InputAttachment
from xerial.Filter import Filter

from typing import Dict, List, Tuple

class SelectInput (Input):
	def __init__(
			self,
			label:str,
			option:List[Tuple[int, str]],
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
			tableDisplayType: TableDisplayType=TableDisplayType.LABEL,
			typeName:str = 'Select',
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
			isAdvanceForm,
			isTableForm,
			isView,
			isSearchTable,
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
		self.option = [list(i) for i in option]
		self.tableDisplayType: TableDisplayType = tableDisplayType
		self.isLink = isLink
		self.isStatusDisplay = isStatusDisplay
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = self.option
		result['isLink'] = self.isLink
		result['isStatusDisplay'] = self.isStatusDisplay
		result['tableDisplayType'] = self.tableDisplayType.value
		return result