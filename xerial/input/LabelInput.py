from xerial.Input import Input

class LabelInput (Input):
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isEditable:bool=True,
			help:str=None,
		) :
		Input.__init__(self, label, order, group, isTable, isSearch, isRequired, isEditable, help)
		self.typeName = 'Label'