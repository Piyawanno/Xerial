from xerial.Input import Input
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
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
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
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.enum = enum
		self.typeName = 'EnumSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = []
		for value in self.enum.label:
			result['option'].append({'label': self.enum.label[value], 'value': value})
		return result