from xerial.Input import Input
from enum import IntEnum
from typing import Type

class EnumSelectInput (Input):
	def __init__(self, label:str, enum:Type[IntEnum], order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False) :
		Input.__init__(self, label, order, isTable, isSearch, isRequired)
		self.enum = enum
		self.typeName = 'EnumSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = []
		for value in self.enum.label:
			result['option'].append({'label': self.enum.label[value], 'value': value})
		return result