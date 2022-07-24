from xerial.Input import Input
from xerial.input.SelectInput import SelectInput

from typing import List, Tuple

class RadioInput (SelectInput):
	def __init__(self,
			label:str,
			option:List[Tuple[int, str]],
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None
		) :
		SelectInput.__init__(self, label, option, order, group, isTable, isSearch, isRequired, isEditable, help)
		self.typeName = 'Radio'

