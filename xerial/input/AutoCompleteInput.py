from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class AutoCompleteInput (ReferenceSelectInput) :
	def __init__(self,
			label:str,
			url:str,
			template:str="",
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
			documentPath:str=None,
		) :
		ReferenceSelectInput.__init__(
			self,
			label,
			url,
			order,
			group,
			isTable,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath
		)
		self.template = template
		self.typeName = 'AutoComplete'

	def toDict(self) -> dict:
		result = super().toDict()
		result['template'] = self.template
		return result