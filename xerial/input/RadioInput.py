from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.input.SelectInput import SelectInput
from xerial.input.TableDisplayType import TableDisplayType
from xerial.Filter import Filter

from typing import Dict, List, Tuple

class RadioInput (SelectInput):
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
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
			isCopyable:bool=False,
			inputPerLine:int=None,
			filter: Filter=None,
			placeHolder:str=None,
			tableDisplayType: TableDisplayType=TableDisplayType.LABEL,
			typeName:str = 'Radio',
		) :
		SelectInput.__init__(
			self,
			label,
			option,
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
			isEnabled=isEnabled,
			isSpreadSheet=isSpreadSheet,
			isCopyable=isCopyable,
			inputPerLine=inputPerLine,
			filter=filter,
			placeHolder=placeHolder,
			tableDisplayType=tableDisplayType,
			typeName=typeName,
		)

