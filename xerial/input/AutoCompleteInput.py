from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class AutoCompleteInput (ReferenceSelectInput) :
	def __init__(self, label:str, url:str, order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False) :
		ReferenceSelectInput.__init__(label, url, order, isTable, isSearch, isRequired)
		self.typeName = 'AutoComplete'