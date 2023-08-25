from typing import Dict
from xerial.Input import Input

class FileMatrixInput (Input):
	def __init__(self,
			label:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isPreview:bool=False,
			isForm:bool=True,
			path:str=None,
			uploadURL:str=None,
			url:str=None,
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
		) :
		Input.__init__(
			self,
			label,
			order,
			group,
			isTable,
			isMobile,
			isSearch,
			isRequired,
			True,
			isForm,
			help,
			documentPath,
			config,
			columnType,
			columnName,
		)
		self.typeName = 'FileMatrix',
		self.isPreview = isPreview
		self.path = path
		self.uploadURL = uploadURL
		self.url = url
		self.isFile = True
	
	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isPreview'] = self.isPreview
		data['path'] = self.path
		data['uploadURL'] = self.uploadURL
		data['url'] = self.url
		data['isFile'] = True
		return data
