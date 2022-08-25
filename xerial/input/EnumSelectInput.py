from xerial.Input import Input
from enum import IntEnum
from typing import Type

class EnumSelectInput (Input):
	def __init__(self,
			label:str,
			enum:Type[IntEnum],
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			documentPath:str=None,
		) :
		Input.__init__(
			self,
			label,
			order,
			group,
			isTable,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath
		)
		self.enum = enum
		self.typeName = 'EnumSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = []
		for value in self.enum.label:
			result['option'].append({'label': self.enum.label[value], 'value': value})
		return result