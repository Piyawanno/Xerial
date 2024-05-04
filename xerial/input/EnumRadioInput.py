from xerial.input.EnumSelectInput import EnumSelectInput
from xerial.InputAttachment import InputAttachment
from enum import IntEnum
from typing import Dict, Type

class EnumRadioInput (EnumSelectInput) :
	def __init__(
			self,
			label:str,
			enum:Type[IntEnum],
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
			typeName:str = 'EnumRadio',
		) :
		EnumSelectInput.__init__(
			self,
			label,
			enum,
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
			isEnabled=isEnabled,
			isSpreadSheet=isSpreadSheet,
			isCopyable=isCopyable,
			typeName=typeName,
		)