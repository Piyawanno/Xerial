from xerial.input.ReferenceSelectInput import ReferenceSelectInput

class ReferenceRadioInput (ReferenceSelectInput) :
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
		ReferenceSelectInput.__init__(label, url, order, group, isTable, isSearch, isRequired, isEditable, help)
		self.typeName = 'ReferenceRadio'