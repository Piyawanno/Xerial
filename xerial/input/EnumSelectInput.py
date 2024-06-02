from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from xerial.OptionEnum import OptionEnum
from enum import IntEnum
from typing import Dict, Type
from xerial.Filter import Filter

class EnumSelectInput (Input):
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
			isAdvanceForm:bool=False,
			isTableForm:bool=False,
			isView:bool=False,
			isSearchTable:bool=False,
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
			typeName:str = 'EnumSelect',
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
			typeName,
		)
		self.enum = enum
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = []
		if issubclass(self.enum, OptionEnum):
			result['option'] = self.enum.toDict()
		else:
			for value in self.enum.label:
				raw = value
				if type(value) != int: raw = value.value
				result['option'].append({'label': self.enum.label[value], 'value': raw})
		return result