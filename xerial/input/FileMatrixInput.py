from typing import Dict
from xerial.Input import Input
from xerial.InputAttachment import InputAttachment

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
			isEditable:bool=True,
			isForm:bool=True,
			isTableForm:bool=False,
			isAdvanceFrom:bool=False,
			isShare:bool=False,
			attachedGroup:InputAttachment=None,
			isLink:bool=False,
			linkColumn:str='',
			path:str=None,
			uploadURL:str=None,
			url:str=None,
			help:str=None,
			documentPath:str=None,
			config:Dict=None,
			columnType:str='',
			columnName:str='',
			isEnabled:bool=True,
			isSpreadSheet:bool=True,
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
			isForm,
			isTableForm,
			isAdvanceFrom,
			attachedGroup,
			isLink,
			linkColumn,
			help,
			documentPath,
			config,
			columnType,
			columnName,
			isEnabled=isEnabled,
			isSpreadSheet=isSpreadSheet,
		)
		self.typeName = 'FileMatrix',
		self.isPreview = isPreview
		self.isShare = isShare
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
		data['isShare'] = self.isShare
		return data
