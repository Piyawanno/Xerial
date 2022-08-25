from xerial.Input import Input

from typing import List, Tuple

class SelectInput (Input):
	def __init__(self,
			label:str,
			option:List[Tuple[int, str]],
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
			documentPath,
		)
		self.option = [list(i) for i in option]
		self.typeName = 'Select'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['option'] = self.option
		return result