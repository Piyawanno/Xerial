from xerial.input.EnumSelectInput import EnumSelectInput
from enum import IntEnum
from typing import Dict, Type

class EnumCheckBoxInput (EnumSelectInput) :
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
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
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
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.typeName = 'EnumCheckBox'