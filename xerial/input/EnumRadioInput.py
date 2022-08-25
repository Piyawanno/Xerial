from xerial.input.EnumSelectInput import EnumSelectInput
from enum import IntEnum
from typing import Type

class EnumRadioInput (EnumSelectInput) :
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
		EnumSelectInput.__init__(
			self,
			label,
			enum,
			order,
			group,
			isTable,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath,
		)
		self.typeName = 'EnumRadio'