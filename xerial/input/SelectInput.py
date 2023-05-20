from xerial.Input import Input

from typing import Dict, List, Tuple

class SelectInput (Input):
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
			help,
			documentPath,
			config
		)
		self.option = [list(i) for i in option]
		self.typeName = 'Select'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = self.option
		return result