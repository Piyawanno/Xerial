from xerial.Input import Input
from xerial.InputAttachment import InputAttachment
from enum import IntEnum
from typing import Dict, Type

class EnumSelectInput (Input):
	def __init__(self,
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
		self.enum = enum
		self.typeName = 'EnumSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = []
		for value in self.enum.label:
			raw = value
			if type(value) != int: raw = value.value
			result['option'].append({'label': self.enum.label[value], 'value': raw})
		return result