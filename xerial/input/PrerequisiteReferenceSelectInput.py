from typing import Dict
from xerial.Input import Input

class PrerequisiteReferenceSelectInput (Input):
	def __init__(self,
			label:str,
			url:str,
			prerequisite: str,
			tableURL:str=None,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			isForm:bool=True,
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
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
			isForm,
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.url = url
		self.tableURL = tableURL
		self.prerequisite = prerequisite
		self.typeName = 'PrerequisiteReferenceSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		result['tableURL'] = self.tableURL
		result['prerequisite'] = self.prerequisite
		return result