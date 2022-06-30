from xerial.Input import Input

class NumberInput (Input):
	def __init__(self, label:str, order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False) :
		Input.__init__(self, label, order, isTable, isSearch, isRequired)
		self.typeName = 'Number'