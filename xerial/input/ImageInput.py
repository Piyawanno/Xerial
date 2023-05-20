from typing import Dict
from xerial.Input import Input

class ImageInput (Input):
	def __init__(self,
			label:str,
			url:str,
			order:str=None,
			group:int=None,
			isTable:bool=False,
			isMobile:bool=False,
			isSearch:bool=False,
			isRequired:bool=False,
			isPreview:bool=False,
			isEditable:bool=True,
			help:str=None,
			path:str=None,
			uploadURL:str=None,
			documentPath:str=None,
			hasCrop:bool=False,
			config:Dict=None
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
			isEditable,
			help,
			documentPath,
			config
		)
		self.url = url
		self.typeName = 'Image',
		self.isPreview = isPreview
		self.path = path
		self.uploadURL = uploadURL
		self.hasCrop = hasCrop
	
	def toDict(self) -> dict :
		data = Input.toDict(self)
		data['isPreview'] = self.isPreview
		data['path'] = self.path
		data['uploadURL'] = self.uploadURL
		data['url'] = self.url
		data['hasCrop'] = self.hasCrop
		return data