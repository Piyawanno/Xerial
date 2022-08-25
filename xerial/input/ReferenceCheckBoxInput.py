from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class ReferenceCheckBoxInput (ReferenceSelectInput) :
	def __init__(self,
			label:str,
			url:str,
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
			label,
			url,
			order,
			group,
			isTable,
			isSearch,
			isRequired,
			isEditable,
			help,
			documentPath,
		)
		self.typeName = 'ReferenceCheckBox'