from typing import Dict
from xerial.Input import Input

class ReferenceSelectInput (Input):
	def __init__(self,
			label:str,
			url:str,
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
		self.url = url
		self.typeName = 'ReferenceSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		return result