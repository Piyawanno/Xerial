from xerial.Input import Input

class PrerequisiteReferenceSelectInput (Input):
	def __init__(self,
			label:str,
			url:str,
			prerequisite: str,
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
			documentPath
		)
		self.url = url
		self.prerequisite = prerequisite
		self.typeName = 'PrerequisiteReferenceSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		result['prerequisite'] = self.prerequisite
		return result