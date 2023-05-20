from xerial.Input import Input
from xerial.input.SelectInput import SelectInput

from typing import Dict, List, Tuple

class CheckBoxInput (SelectInput):
	def __init__(self,
			label:str,
			option:List[Tuple[int, str]],
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			documentPath:str=None,
			config:Dict=None
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
			help,
			documentPath,
			config
		)
		self.typeName = 'CheckBox'

