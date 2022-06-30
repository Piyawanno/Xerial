from xerial.input.EnumSelectInput import EnumSelectInput
from enum import IntEnum
from typing import Type

class EnumRadioInput (EnumSelectInput) :
	def __init__(self, label:str, enum:Type[IntEnum], order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False) :
		EnumSelectInput.__init__(self, label, enum, order, isTable, isSearch, isRequired)
		self.typeName = 'EnumRadio'