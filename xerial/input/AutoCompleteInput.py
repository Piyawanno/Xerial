from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class AutoCompleteInput (ReferenceSelectInput) :
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
		) :
		ReferenceSelectInput.__init__(self, label, url, group, order, isTable, isSearch, isRequired, isEditable, help)
		self.typeName = 'AutoComplete'