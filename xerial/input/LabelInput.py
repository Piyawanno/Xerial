from xerial.Input import Input

class LabelInput (Input):
	def __init__(self, label:str, order:str=None, isTable:bool=False, isSearch:bool=False) :
		Input.__init__(self, label, order, isTable, isSearch)
		self.typeName = 'Label'