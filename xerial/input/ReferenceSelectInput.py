from xerial.Input import Input

class ReferenceSelectInput (Input):
	def __init__(self, label:str, url:str, order:str=None, isTable:bool=False, isSearch:bool=False, isRequired:bool=False) :
		Input.__init__(self, label, order, isTable, isSearch, isRequired)
		self.url = url
		self.typeName = 'ReferenceSelect'
	
	def toDict(self) -> dict:
		result = super().toDict()
		result['url'] = self.url
		return result