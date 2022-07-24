from xerial.Input import Input

class FileMatrixInput (Input):
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isPreview:bool=False,
			path:str=None,
			uploadURL:str=None,
		) :
		Input.__init__(self, label, order, group, isTable, isSearch, isRequired)
		self.typeName = 'FileMatrix',
		self.isPreview = isPreview
		self.path = path
		self.uploadURL = uploadURL
	
	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isPreview'] = self.isPreview
		data['path'] = self.path
		data['uploadURL'] = self.uploadURL
		return data
